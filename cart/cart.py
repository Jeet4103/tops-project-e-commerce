from store.models import Products, Profile
import json

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('cart')

        if 'cart' not in self.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user_id=self.request.user.id)
            current_user.update(old_cart=json.dumps(self.cart))

    def db_add(self, product, quantity, size=None):
        product_id = str(product.id)
        key = f"{product_id}_{size}" if size else product_id

        if key in self.cart:
            self.cart[key]['quantity'] += quantity
        else:
            self.cart[key] = {
                'name': product.name,
                'price': str(product.sale_price if getattr(product, 'is_sales', False) else product.price),
                'quantity': quantity,
                'image': product.thumbnail.url if product.thumbnail else None,
                'size': size
            }

        self.save()

    def add(self, product, size=None, quantity=1):
        self.db_add(product, quantity, size)

    def delete(self, product_id, size=None):
        key = f"{product_id}_{size}" if size else str(product_id)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = [key.split('_')[0] for key in self.cart.keys()]
        products = Products.objects.filter(id__in=product_ids)

        product_list = []
        for key, product_data in self.cart.items():
            product_id = key.split('_')[0]
            quantity = product_data['quantity']
            if isinstance(quantity, dict):
                quantity = int(quantity.get('value', 1))
            else:
                quantity = int(quantity)

            price = float(product_data['price'])
            size = product_data.get('size')

            product = next((p for p in products if str(p.id) == product_id), None)
            if product:
                product_list.append({
                    'id': product.id,
                    'name': product.name,
                    'thumbnail': product.thumbnail,
                    'quantity': quantity,
                    'price': price,
                    'size': size,
                })

        return product_list

    def merge_old_cart(self, old_cart_json):
        if not old_cart_json:
            return
        try:
            old_cart = json.loads(old_cart_json)
        except Exception:
            old_cart = {}

        # Instead of only adding missing keys, overwrite quantities for keys present in both carts
        for key, val in old_cart.items():
            if key in self.cart:
                # Optional: sum quantities or just overwrite? Overwrite is safer here to avoid duplicates
                self.cart[key]['quantity'] = val['quantity']
            else:
                self.cart[key] = val

        self.save()