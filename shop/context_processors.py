from .cart import Cart

def cart(request):
    """Rend le panier disponible dans tous les templates HTML."""
    return {'cart': Cart(request)}