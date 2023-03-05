from django.contrib import admin
from . import models
from fpdf import FPDF
# Register your models here.
class ProductAdminSite(admin.ModelAdmin):
    model = models.Product
    list_display = ['title', 'price','last_updated']
    actions = ["get_list"]

    def get_list(self, request, queryset):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 10, txt = "products details:-",
                    ln = 1, align = 'L')
        for product in queryset:
            pdf.cell(200, 10, txt = str(product.title)+"     "+str(product.price),
                    ln = 1, align = 'L')

        pdf.output("productdetails.pdf") 
            

class OrderAdminSite(admin.ModelAdmin):
    model = models.Order
    list_display = ['customer', 'address', 'order_status', 'payment_status','placed_at']
    actions = ["get_recept"]

    def get_recept(self, request, queryset):
        for order in queryset:
            user = order.customer
            add = order.address
            date = order.placed_at
            ref = order.reference
            paymentid = order.razorpay_payment_id
            order_items = order.orderitem_set.all()
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size = 15)
            pdf.cell(200, 10, txt = "customer name : "+ str(user),
                    ln = 1, align = 'L')
            pdf.cell(200, 10, txt = "Reference : "+ str(ref),
                    ln = 1, align = 'L')
            pdf.cell(200, 10, txt = "address : " + str(add),
                    ln = 2, align = 'L')
            pdf.cell(200, 10, txt = "Order place at" + str(date),
                    ln = 2, align = 'L')
            pdf.cell(200, 10, txt = "payment_id : " + str(paymentid),
                    ln = 2, align = 'L')
            pdf.cell(200, 10, txt = "Order Items:-",
                    ln = 2, align = 'L')
            for items in order_items:
                pdf.cell(200, 10, txt = str(items),
                        ln = 2, align = 'L')
            pdf.output(str(user)+".pdf")

admin.site.register(models.Address)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Collection)
admin.site.register(models.Customer)
admin.site.register(models.Order, OrderAdminSite)
admin.site.register(models.OrderItem)
admin.site.register(models.Tag)
admin.site.register(models.Product, ProductAdminSite)
admin.site.register(models.ProductImages)








