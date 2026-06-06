from database.product_repo import (get_product_by_code,save_product)

# اطلاعات مشتری
def get_customer_data():
    user_data = {
        "customer_name": input("نام مشتری : "),
        "customer_phone": input("شماره مشتری : "),
        "customer_address": input("آدرس مشتری : "),
        "invoice_number": input("شماره فاکتور : "),
        "customer_national_code": input("کد ملی مشتری : "),
        "customer_economic_code": input("شماره اقتصادی مشتری : "),
        "customer_postal_code": input("کد پستی مشتری : "),
    }
    return user_data

def get_items():
    items = []
    count = int(input("چند کالا ثبت می‌کنید؟ : "))
    for i in range(count):
        print("\n")
        print("=" * 50)
        print(f"کالای شماره {i+1}")
        print("=" * 50)
        code = input("کد کالا : ")
        product = get_product_by_code(code)
        if product:
            print(f"کالا انتخاب شد: {product[2]} | قیمت: {product[3]}")
            qty = int(input("تعداد : "))
            items.append({
                "code": product[1],
                "name": product[2],
                "qty": qty,
                "price": product[3]
            })
        else:
            print("کالا پیدا نشد! باید ثبت شود")
            name = input("نام کالا : ")
            price = int(input("قیمت : "))
            description = input("توضیحات : ")
            save_product({
                "code": code,
                "name": name,
                "price": price,
                "description": description
            })
            qty = int(input("تعداد : "))
            items.append({
                "code": code,
                "name": name,
                "qty": qty,
                "price": price
            })
    return items