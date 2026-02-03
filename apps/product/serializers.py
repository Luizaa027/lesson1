from rest_framework import serializers
from apps.product.models import Product, Category, Models, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image',  ]


class ProductSerializer(serializers.ModelSerializer):
    first_images = serializers.SerializerMethodField() 

    class Meta: 
        model = Product 
        fields = [ 
            "id",
            "uutd",
            "title",
            "description",
            "price",
            "first_images",
        ]        
    def get_first_images(self, onj):
        first_images = onj.images.first()
        if first_images:
            return first_images.image.url
        return None 
    

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)
    model_title = serializers.CharField(source='model.title', read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "uutd",
            "title",
            "description",
            "price",
            "size",
            "is_active",
            "is_favorite",
            "created_at",
            "images",
            "category_title",
            "model_title",
        ]   

class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False , 

    )
    class Meta:
        model = Product
        fields = [
            "category",
            "model",
            "title",
            "description",
            "price",
            "size",
            "images",
        ] 
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Название должно быть больше 3 символов") 
        return value 
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля")
        return value
    
    def validate_size(self, value):
        if len(value) > 10 :
            raise serializers.ValidationError("Размер слишком большой") 
        return value 
    
    def validate(self, attrs):
        category = attrs.get("category")  
        model = attrs.get("model")
      
        if model and category and model.category != category:
            raise serializers.ValidationError(
                "Модель не соответствует категории"
            ) 
        return attrs 

    def create(self, validate_data):
        images_data = validate_data.pop("images ", [])
        product = Product.objects.create(**validate_data)

        for imag in images_data:
            ProductImage.objects.create(product=product, image=imag)
        return product 