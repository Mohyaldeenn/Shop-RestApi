from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product


@receiver([post_delete, post_save], sender = Product)
def invalidate_product_cache(sender, instance, **kwargs) :
    """invalidate product cache when product deleted or updated"""
    print("clearing product cache")
    
    # clear product list caches
    cache.delete_pattern("*product_list*")
