from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)  # Corrigé ici
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    nom = models.CharField(max_length=200)  # Corrigé ici
    description = models.TextField(blank=True)
    prix = models.IntegerField()
    stock = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom