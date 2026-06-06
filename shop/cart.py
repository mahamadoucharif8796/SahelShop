from decimal import Decimal
from .models import Produit


class Cart:
    def __init__(self, request):
        """Initialise le panier à partir de la session Django."""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Si le panier n'existe pas encore, on en crée un vide
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, produit, quantite=1):
        """Ajoute un produit au panier ou augmente sa quantité."""
        produit_id = str(produit.id)
        if produit_id not in self.cart:
            self.cart[produit_id] = {'quantite': 0, 'prix': str(produit.prix)}

        self.cart[produit_id]['quantite'] += quantite
        self.save()

    def remove(self, produit):
        """Supprime un produit du panier."""
        produit_id = str(produit.id)
        if produit_id in self.cart:
            del self.cart[produit_id]
            self.save()

    def save(self):
        """Marque la session comme modifiée pour enregistrer les changements."""
        self.session.modified = True

    def get_total_price(self):
        """Calcule le montant total du panier."""
        return sum(Decimal(item['prix']) * item['quantite'] for item in self.cart.values())

    def clear(self):
        """Vide complètement le panier."""
        del self.session['cart']
        self.save()

    def __len__(self):
        """Compte le nombre total d'articles dans le panier."""
        return sum(item['quantite'] for item in self.cart.values())