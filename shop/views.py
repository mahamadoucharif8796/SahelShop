from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Categorie
from .cart import Cart


# Page d'accueil
def index(request):
    # On récupère tous les produits disponibles et toutes les catégories
    produits = Produit.objects.filter(disponible=True)
    categories = Categorie.objects.all()

    # 1. Gestion de la Recherche (si le client tape quelque chose)
    query = request.GET.get('search')
    if query:
        produits = produits.filter(nom__icontains=query) # Recherche insensible à la casse

    # 2. Gestion du Filtrage par Catégorie (si le client clique sur une catégorie)
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        produits = produits.filter(categorie_id=categorie_id)

    return render(request, 'shop/index.html', {
        'produits': produits,
        'categories': categories,
        'query': query,
        'categorie_actuelle': int(categorie_id) if categorie_id else None
    })

# Page de détail
def detail_produit(request, id):
    produit = get_object_or_404(Produit, id=id, disponible=True)
    return render(request, 'shop/detail.html', {'produit': produit})


# Action : Ajouter au panier
def cart_add(request, produit_id):
    cart = Cart(request)
    produit = get_object_or_404(Produit, id=produit_id)
    cart.add(produit=produit)

    # Redirige sur la page actuelle au lieu d'aller directement au panier
    return redirect(request.META.get('HTTP_REFERER', 'index'))


# Action : Supprimer du panier
def cart_remove(request, produit_id):
    cart = Cart(request)
    produit = get_object_or_404(Produit, id=produit_id)
    cart.remove(produit)
    return redirect('cart_detail')


# Page du Panier
import urllib.parse  # À ajouter tout en haut du fichier pour encoder le texte du message


def cart_detail(request):
    cart = Cart(request)
    cart_items = []

    # On prépare le début de notre texte de commande pour WhatsApp
    texte_commande = "Bonjour SahelShop ! Je souhaite commander les articles suivants :\n\n"

    for produit_id, item in cart.cart.items():
        produit = Produit.objects.get(id=int(produit_id))
        total_item = produit.prix * item['quantite']

        cart_items.append({
            'produit': produit,
            'quantite': item['quantite'],
            'total_item': total_item
        })

        # On ajoute chaque produit au texte du message
        texte_commande += f"- {produit.nom} (Qté : {item['quantite']}) : {total_item} FCFA\n"

    total_panier = cart.get_total_price()
    texte_commande += f"\n*Montant Total : {total_panier} FCFA*"

    # On encode le texte pour qu'il soit lisible dans une URL web
    whatsapp_message = urllib.parse.quote(texte_commande)

    # METS TON NUMÉRO ICI (ex: 22790000000 sans le +)
    numero_whatsapp = "22787960393"

    link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={whatsapp_message}"

    return render(request, 'shop/cart_detail.html', {
        'cart_items': cart_items,
        'total_panier': total_panier,
        'link_whatsapp': link_whatsapp
    })


# Action : Mettre à jour la quantité d'un produit
def cart_update(request, produit_id):
    cart = Cart(request)
    produit = get_object_or_404(Produit, id=produit_id)

    # On récupère la quantité envoyée par le formulaire (par défaut 1)
    try:
        quantite = int(request.POST.get('quantite', 1))
        if quantite > 0:
            # On réinitialise la quantité à la valeur choisie
            cart.cart[str(produit.id)]['quantite'] = quantite
            cart.save()
        else:
            cart.remove(produit)
    except ValueError:
        pass

    return redirect('cart_detail')


# Action : Vider tout le panier
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')