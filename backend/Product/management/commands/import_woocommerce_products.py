from django.core.management.base import BaseCommand
from woocommerce import API
from Product.models import (
    Product, Category, Brand, Tag, Attribute, AttributeValue,
    ProductImage, ProductVariation
)
from django.utils.html import strip_tags
from django.utils import timezone
import dateutil.parser
import requests
from django.core.files.base import ContentFile
import os


class Command(BaseCommand):
    help = "Import 50 products from WooCommerce into DRF"

    def handle(self, *args, **kwargs):
        wcapi = API(
            url="",
            consumer_key="ck_5bf950ecece9fd819c298f0d8fa62f90e807e907",
            consumer_secret="cs_4a86476f14cc0b2758020c4b1d81f9b30f146ee6",
            version="wc/v3"
        )

        products = wcapi.get("products", params={"per_page": 50, "page": 1}).json()

        for p in products:
            # -------------------
            # Category
            # -------------------
            category_name = p["categories"][0]["name"] if p.get("categories") else None
            category = None
            if category_name:
                category, _ = Category.objects.get_or_create(
                    name=category_name,
                    defaults={"slug": category_name.lower().replace(" ", "-")}
                )

            # -------------------
            # Brand
            # -------------------
            brand = None
            for attr in p.get("attributes", []):
                if attr["name"].lower() == "brand" and attr.get("options"):
                    brand_name = attr["options"][0]
                    brand, _ = Brand.objects.get_or_create(
                        name=brand_name,
                        defaults={"slug": brand_name.lower().replace(" ", "-")}
                    )

            # -------------------
            # Featured Image
            # -------------------
            featured_image_url = p.get("images")[0]["src"] if p.get("images") else None

            # -------------------
            # Meta fields
            # -------------------
            meta_title = ""
            meta_description = ""
            for meta in p.get("meta_data", []):
                if meta.get("key") == "_yoast_wpseo_title":
                    meta_title = meta.get("value")
                elif meta.get("key") == "_yoast_wpseo_metadesc":
                    meta_description = meta.get("value")

            # -------------------
            # Created & Updated dates
            # -------------------
            created_at = None
            updated_at = None
            if p.get("date_created"):
                created_at = timezone.make_aware(dateutil.parser.isoparse(p["date_created"]))
            if p.get("date_modified"):
                updated_at = timezone.make_aware(dateutil.parser.isoparse(p["date_modified"]))

            # -------------------
            # Product
            # -------------------
            sku_value = p.get("sku") or None

            product, _ = Product.objects.update_or_create(
                slug=p["slug"],
                defaults={
                    "name": p["name"],
                    "sku": sku_value,
                    "description": strip_tags(p.get("description") or p.get("short_description") or ""),
                    "price": float(p.get("price") or 0),
                    "discount_price": float(p.get("sale_price") or 0) if p.get("sale_price") else None,
                    "tax": 10 if p.get("tax_class") == "standard" else 0,
                    "stock": p.get("stock_quantity") or 0,
                    "category": category,
                    "brand": brand,
                    "is_active": p.get("status") == "publish",
                    "video_url": p.get("video_url", ""),
                    "meta_title": meta_title,
                    "meta_description": meta_description,
                    "featured_image": None,  # will save below
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "weight": float(p.get("weight") or 0),
                    "length": float(p.get("dimensions", {}).get("length") or 0),
                    "width": float(p.get("dimensions", {}).get("width") or 0),
                    "height": float(p.get("dimensions", {}).get("height") or 0),
                }
            )

            # -------------------
            # Save featured image
            # -------------------
            if featured_image_url:
                try:
                    response = requests.get(featured_image_url)
                    if response.status_code == 200:
                        product.featured_image.save(
                            os.path.basename(featured_image_url),
                            ContentFile(response.content),
                            save=True
                        )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Failed to save featured image: {e}"))

            # -------------------
            # Tags
            # -------------------
            tags = []
            for t in p.get("tags", []):
                tag, _ = Tag.objects.get_or_create(
                    name=t["name"],
                    defaults={"slug": t["slug"]}
                )
                tags.append(tag)
            product.tags.set(tags)

            # -------------------
            # Attributes
            # -------------------
            attributes = []
            for attr in p.get("attributes", []):
                attribute, _ = Attribute.objects.get_or_create(name=attr["name"])
                for val in attr.get("options", []):
                    attr_val, _ = AttributeValue.objects.get_or_create(attribute=attribute, value=val)
                    attributes.append(attr_val)
            product.attributes.set(attributes)

            # -------------------
            # Gallery Images
            # -------------------
            for img in p.get("images", []):
                try:
                    response = requests.get(img["src"])
                    if response.status_code == 200:
                        ProductImage.objects.create(
                            product=product,
                            image=ContentFile(response.content, name=os.path.basename(img["src"])),
                            alt=img.get("alt", "")
                        )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Failed to save gallery image: {e}"))

            # -------------------
            # Variations
            # -------------------
            for var_id in p.get("variations", []):
                variation_data = wcapi.get(f"products/{p['id']}/variations/{var_id}").json()
                variation_sku = variation_data.get("sku") or None

                variation, _ = ProductVariation.objects.update_or_create(
                    sku=variation_sku,
                    defaults={
                        "product": product,
                        "price": float(variation_data.get("price") or 0),
                        "discount_price": float(variation_data.get("sale_price") or 0) if variation_data.get("sale_price") else None,
                        "stock": variation_data.get("stock_quantity") or 0,
                        "is_active": variation_data.get("status") == "publish",
                    }
                )

                # Variation attributes
                attrs = []
                for av in variation_data.get("attributes", []):
                    attribute, _ = Attribute.objects.get_or_create(name=av["name"])
                    attr_val, _ = AttributeValue.objects.get_or_create(attribute=attribute, value=av["option"])
                    attrs.append(attr_val)
                variation.attributes.set(attrs)

        self.stdout.write(self.style.SUCCESS("✅ 50 Products imported successfully with all fields"))
