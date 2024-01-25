from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from logintohome.models import CustomUser1
from todelivery.models import order_details, ordered_items, address
from product_manage.models import products
from django.http import HttpResponseServerError
from datetime import date, timedelta
from django.db.models import Sum, Count
from datetime import datetime
from django.db.models import Q
from datetime import datetime
from product_manage.models import variant
from userprofile.models import wallet, return_requests
from category_management.models import category
from .models import product_offer, category_offer
from django.db.models import Q

# Create your views here.


# admin login
@never_cache
def admin_login(request):
    if "email" not in request.session:
        if "username" in request.session:
            return redirect("adminhome")
        if request.method == "POST":
            username = request.POST["name"]
            password = request.POST["pass"]
            obj = authenticate(username=username, password=password)
            if obj is not None:
                request.session["username"] = username
                messages.success(request, "you are welcome.....!")
                return redirect("adminhome")
            else:
                messages.error(request, "enter a valid username or password")
                return redirect("adminlogin")
        return render(request, "admin_login.html")
    else:
        return render(request, "404.html", status=404)


# admin home


@never_cache
def admin_home(request):
    if "email" not in request.session:
        if "username" in request.session:
            today = date.today()
            year = date.today().year
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            current_date = datetime.now().date()
            print("Current Date:", current_date)
            thismonth = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=date.today().month,
            ).aggregate(sum=Sum("total_amount"))
            today = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date=today,
            ).aggregate(sum=Sum("total_amount"))
            thisyear = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__year=year,
            ).aggregate(sum=Sum("total_amount"))
            thisweek = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__range=[start_week, end_week],
            ).aggregate(sum=Sum("total_amount"))
            jan = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=1,
            ).aggregate(sum=Sum("total_amount"))
            feb = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=2,
            ).aggregate(sum=Sum("total_amount"))
            mar = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=3,
            ).aggregate(sum=Sum("total_amount"))
            apr = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=4,
            ).aggregate(sum=Sum("total_amount"))
            may = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=5,
            ).aggregate(sum=Sum("total_amount"))
            june = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=6,
            ).aggregate(sum=Sum("total_amount"))
            july = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=7,
            ).aggregate(sum=Sum("total_amount"))
            aug = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=8,
            ).aggregate(sum=Sum("total_amount"))
            sep = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=9,
            ).aggregate(sum=Sum("total_amount"))
            oct = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=10,
            ).aggregate(sum=Sum("total_amount"))
            nov = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=11,
            ).aggregate(sum=Sum("total_amount"))
            dec = ordered_items.objects.filter(
                Q(status="delivered")
                | Q(status="return requested")
                | Q(status="return denied"),
                order_id__order_date__month=12,
            ).aggregate(sum=Sum("total_amount"))

            if thismonth["sum"] is None:
                thismonth["sum"] = 0
            if today["sum"] is None:
                today["sum"] = 0
            if thisyear["sum"] is None:
                thisyear["sum"] = 0
            if thisweek["sum"] is None:
                thisweek["sum"] = 0
            if jan["sum"] is None:
                jan["sum"] = 0
            daily_sales_data = []
            for i in range(7):
                date_in_week = start_week + timedelta(days=i)
                daily_sale = ordered_items.objects.filter(
                    Q(status="delivered")
                    | Q(status="return requested")
                    | Q(status="return denied"),
                    order_id__order_date=date_in_week,
                ).aggregate(sum=Sum("total_amount"))
                daily_sales_data.append(daily_sale["sum"] if daily_sale["sum"] else 0)

            context = {
                "thismonth": thismonth,
                "today": today,
                "thisyear": thisyear,
                "thisweek": thisweek,
                "jan": jan,
                "feb": feb,
                "mar": mar,
                "apr": apr,
                "may": may,
                "june": june,
                "july": july,
                "aug": aug,
                "sep": sep,
                "oct": oct,
                "nov": nov,
                "dec": dec,
                "date": current_date,
                "daily_sales_data": daily_sales_data,
            }
            return render(request, "admin_home.html", context)
        else:
            return redirect("adminlogin")
    else:
        return render(request, "404.html", status=404)


# admin  logout
@never_cache
def admin_logout(request):
    if "username" in request.session:
        request.session.flush()
    return redirect("adminlogin")


# user manage


def user_manage(request):
    if "email" not in request.session:
        if "username" in request.session:
            user = CustomUser1.objects.all()
            context = {"user": user}

            return render(request, "user_management.html", context)
    else:
        return render(request, "404.html", status=404)


# block user


def block_user(request, id):
    if "username" in request.session:
        obj = CustomUser1.objects.get(id=id)
        obj.is_blocked = True
        obj.save()
        return redirect("usermanage")


# un block user


def un_block_user(request, id):
    if "username" in request.session:
        obj = CustomUser1.objects.get(id=id)
        obj.is_blocked = False
        obj.save()
        return redirect("usermanage")


# search for user


def search_for_user(request):
    if "username" in request.session:
        if request.method == "POST":
            query = request.POST["query"]
            user = CustomUser1.objects.filter(username__icontains=query)
            context = {
                "user": user,
            }
        return render(request, "user_management.html", context)


# order management


def order_management(request):
    if "email" not in request.session:
        if "username" in request.session:
            obj = order_details.objects.all().order_by("-id")
            context = {
                "items": obj,
            }
            return render(request, "order_management.html", context)
        else:
            return redirect("adminlogin")
    else:
        return render(request, "404.html", status=404)


#
def more_details_in_admin(request, id):
    obj = ordered_items.objects.filter(order_id_id=id)
    context = {
        "orders": obj,
    }
    return render(request, "more_details_order.html", context)


# edit status
def edit_status(request, id):
    if request.method == "POST":
        changestatus = request.POST["changestatus"]
        obj = ordered_items.objects.get(id=id)
        obj.status = changestatus
        obj.save()
        messages.success(request, "your status is edited successfully....!")
    return redirect("moredetailsinadmin", obj.order_id_id)


# cancel order
def cancel_order(request, id):
    obj = ordered_items.objects.get(id=id)
    obj.status = "cancelled by admin"
    pro = variant.objects.get(product_id=obj.product_name, id=obj.size.id)
    pro.quantity = pro.quantity + obj.quantity
    obj.save()
    pro.save()
    if (
        obj.order_id.pay_method == "razor_pay"
        or obj.order_id.pay_method == "wallet_pay"
    ):
        if obj.order_id.coupen_applyed == True:
            wall = wallet.objects.get(user_id=obj.order_id.user_id)
            print(obj.order_id.id)
            my_dict = ordered_items.objects.filter(
                order_id_id=obj.order_id.id
            ).aggregate(no=Count("id"))
            no_orders = my_dict["no"]
            discount = obj.order_id.applied_coupen.cop_price
            print(discount)
            for_each_pro = int(discount / no_orders)
            rtrn_to_wlt = obj.total_amount - for_each_pro
            wall.amount = wall.amount + rtrn_to_wlt
            print(wall)
            wall.save()
            messages.success(request, " order cacelled successfully")
            return redirect("ordersmanage")
        else:
            wall = wallet.objects.get(user_id=obj.order_id.user_id)
            wall.amount = wall.amount + obj.total_amount
            wall.save()
            messages.success(request, " order cacelled successfully")
            return redirect("ordersmanage")
    return redirect("ordersmanage")


# sales report
def sales_report(request):
    if request.method == "POST":
        start = request.POST["date1"]
        print(start)
        end = request.POST["date2"]
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if end_date > start_date:
            obj = ordered_items.objects.filter(
                Q(status="delivered") & Q(order_id__order_date__range=[start, end])
            )
        else:
            messages.error(request, "select valid date....")
            return redirect("adminhome")
        print(obj)
    return render(request, "sales_report.html", {"orders": obj})


############################################             offer management             ########################################################


# add product offer
def product_offers(request):
    pros = products.objects.filter(is_listed=True)
    context = {
        "pros": pros,
    }
    if request.method == "POST":
        pro = request.POST["pro"]
        persc = int(request.POST["perc"])
        others = product_offer.objects.filter(pro_id = pro)
        h = []
        for i in others:
            h.append(i.pro_id.id)
        print("the list is", h)
        if int(pro) not in h:
            if persc <= 100 and persc >= 0:
                print(pro)
                print(persc)
                prod = products.objects.get(id=pro)
                product_offer.objects.create(pro_id=prod, percentage=persc)
                messages.success(request, "product offer added successfully")
                return redirect("productoffer")
            messages.success(request, "the percentage should between 0 and 100")
            return redirect("productoffer")
        messages.success(request, "the offer for this product is already added")
        return redirect("productoffer")
    return render(request, "product_offer.html", context)


# category offer
def category_offers(request):
    cats = category.objects.filter(is_listed=True)
    context = {
        "cats": cats,
    }

    if request.method == "POST":
        pro = request.POST["category"]
        persc = int(request.POST["perc"])
        others = category_offer.objects.filter(cat_id=pro)
        h = []
        for i in others:
            h.append(i.cat_id.id)
        print("the list is", h)
        if int(pro) not in h:
            if persc <= 100 and persc >= 0:
                prod = category.objects.get(id=pro)
                category_offer.objects.create(cat_id=prod, percentage=persc)
                messages.success(request, "product offer added successfully")
                return redirect("categoryoffer")
            messages.success(request, "the percentage should between 0 and 100")
            return redirect("categoryoffer")
        messages.success(request, "the offer for this category is already added")
        return redirect("categoryoffer")
    return render(request, "category_offer.html", context)


# view product offer
def view_product_offer(request):
    if "email" not in request.session:
        if "username" in request.session:
            items = product_offer.objects.all()
            context = {
                "items": items,
            }
            return render(request, "view_product_offer.html", context)
        else:
            return redirect("adminlogin")
    else:
        return render(request, "404.html", status=404)


# view category offer
def view_category_offer(request):
    if "email" not in request.session:
        if "username" in request.session:
            items = category_offer.objects.all()
            context = {
                "items": items,
            }
            return render(request, "view_category_offer.html", context)
        else:
            return redirect("adminlogin")
    else:
        return render(request, "404.html", status=404)


# edit product offer
def edit_product_offer(request, id):
    if request.method == "POST":
        pesc = int(request.POST["pesc"])
        if pesc <= 100 and pesc >= 0:
            obj = product_offer.objects.get(id=id)
            obj.percentage = pesc
            obj.save()
            messages.success(request, "product offer edited successfully")
            return redirect("viewproductoffer")
    messages.success(request, "the percentage should between 0 and 100")
    return redirect("viewproductoffer")


# edit category offer
def edit_category_offer(request, id):
    if request.method == "POST":
        pesc = int(request.POST["pesc"])
        if pesc <= 100 and pesc >= 0:
            obj = category_offer.objects.get(id=id)
            obj.percentage = pesc
            obj.save()
            messages.success(request, "category offer edited successfully")
            return redirect("viewcategoryoffer")
    messages.success(request, "the percentage should between 0 and 100")
    return redirect("viewcategoryoffer")


# list category offer
def list_category_offer(request, id):
    obj = category_offer.objects.get(id=id)
    obj.is_listed = True
    obj.save()
    return redirect("viewcategoryoffer")


# unlist category offer
def un_list_category_offer(request, id):
    obj = category_offer.objects.get(id=id)
    obj.is_listed = False
    obj.save()
    return redirect("viewcategoryoffer")


# list product offer
def list_product_offer(request, id):
    obj = product_offer.objects.get(id=id)
    obj.is_listed = True
    obj.save()
    return redirect("viewproductoffer")


# unlist category offer
def un_list_product_offer(request, id):
    obj = product_offer.objects.get(id=id)
    obj.is_listed = False
    obj.save()
    return redirect("viewproductoffer")


# return management
def return_management(request):
    returns = return_requests.objects.all().order_by("-id")
    context = {"returns": returns}
    return render(request, "return_management.html", context)


# change return management and incresing wallet and incresing the quantity
def change_return_status(request, id):
    return_obj = return_requests.objects.get(id=id)
    print(return_obj.reason)
    if request.method == "POST":
        status = request.POST["status"]
        ordered_item = ordered_items.objects.get(id=return_obj.item_id.id)
        order = order_details.objects.get(id=ordered_item.order_id.id)
        if status == "return accepted":
            if order.pay_method == "razor_pay" or order.pay_method == "wallet_pay":
                userwal = wallet.objects.get(user_id=ordered_item.order_id.user_id)
                my_dict = ordered_items.objects.filter(
                    order_id_id=return_obj.order_id.id
                ).aggregate(no=Count("id"))
                no_orders = my_dict["no"]
                if return_obj.order_id.coupen_applyed == True:
                    discount = return_obj.order_id.applied_coupen.cop_price
                    for_each_pro = int(discount / no_orders)
                    rtrn_to_wlt = return_obj.item_id.total_amount - for_each_pro
                    userwal.amount = userwal.amount + rtrn_to_wlt
                    pro = variant.objects.get(id=ordered_item.size.id)
                    pro.quantity = pro.quantity + ordered_item.quantity
                    pro.save()
                    userwal.save()
                    ordered_item.status = status
                    ordered_item.save()
                    messages.success(
                        request,
                        "status updated successfully amount sent to user wallet",
                    )
                    return redirect("returnmanagement")
                userwal.amount = userwal.amount + ordered_item.total_amount
                ordered_item.status = status
                pro = variant.objects.get(id=ordered_item.size.id)
                pro.quantity = pro.quantity + ordered_item.quantity
                pro.save()
                ordered_item.save()
                userwal.save()
                messages.success(
                    request, "status updated successfully amount sent to user wallet"
                )
                return redirect("returnmanagement")
            pro = variant.objects.get(id=ordered_item.size.id)
            pro.quantity = pro.quantity + ordered_item.quantity
            ordered_item.status = status
            ordered_item.save()
            pro.save()
            messages.success(request, "status updated successfully")
            return redirect("returnmanagement")
        ordered_item.status = status
        ordered_item.save()
        messages.success(request, "status updated successfully")
        return redirect("returnmanagement")



