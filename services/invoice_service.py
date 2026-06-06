from core.customer_input import (
    get_customer_data,
    get_items
)
from core.calculator import (
    calculate_total,
    calculate_tax,
    calculate_final
)
from core.invoice_generator import (
    render_html,
    save_html,
    generate_pdf
)
from database.customer_repo import (
    save_customer,
    get_customer_by_phone
)
from database.invoice_repo import (
    save_invoice,
    save_invoice_item
)
from config.settings import (
    TAX_RATE,
    COMPANY_NAME,
    COMPANY_PHONE,
    COMPANY_ADDRESS,
    TEMPLATE_DIR,
    OUTPUT_HTML_DIR,
    OUTPUT_PDF_DIR,
    WKHTMLTOPDF_PATH
)
from database.invoice_repo import (
    save_invoice
)
import os
import jdatetime

def create_invoice():
    # ==========================================
    # اطلاعات ثابت شرکت

    fixed_data = {
        "company_name": COMPANY_NAME,
        "company_phone": COMPANY_PHONE,
        "company_address": COMPANY_ADDRESS
    }
    # ==========================================
    # اطلاعات مشتری
    user_data = get_customer_data()
    
    customer = get_customer_by_phone(
        user_data["customer_phone"]
    )
    
    if customer:
    
        customer_id = customer[0]
    
        user_data = {
    
            "customer_name":             customer[1],
            "customer_phone":            customer[2],
            "customer_national_code":    customer[3],
            "customer_economic_code":    customer[4],
            "customer_postal_code":      customer[5],
            "customer_address":          customer[6],
        }
    
    else:
    
        customer_id = save_customer(
            user_data
        )

    # ==========================================
    # کالاها

    items = get_items()

    # ==========================================
    # محاسبات

    total_price = calculate_total(items)

    tax = calculate_tax(
        total_price,
        TAX_RATE
    )

    final_price = calculate_final(
        total_price,
        tax
    )

    # ==========================================
    # تاریخ

    invoice_date = jdatetime.date.today().strftime(
        "%Y/%m/%d"
    )
    
    invoice_data = {
        "invoice_number": user_data["invoice_number"],
        "invoice_date": invoice_date,
        "customer_id": customer_id,
        "total_price": total_price,
        "tax": tax,
        "final_price": final_price
    }
    invoice_id = save_invoice(
        invoice_data
    )

    print(
        f"Invoice Saved => ID:{invoice_id}"
    )

    for item in items:
    
        save_invoice_item(
            invoice_id,
            item
        )
    # ==========================================
    # Context

    context = {

        **fixed_data,

        **user_data,

        "invoice_date": invoice_date,

        "items": items,

        "total_price": total_price,

        "tax": tax,

        "final_price": final_price,
    }

    # ==========================================
    # ساخت HTML

    html_content = render_html(
        TEMPLATE_DIR,
        "factor_1.html",
        context
    )

    output_html = os.path.join(
        OUTPUT_HTML_DIR,
        "invoice.html"
    )

    save_html(
        html_content,
        output_html
    )

    # ==========================================
    # ساخت PDF

    output_pdf = os.path.join(
        OUTPUT_PDF_DIR,
        "invoice.pdf"
    )

    generate_pdf(
        output_html,
        output_pdf,
        WKHTMLTOPDF_PATH
    )

    # ==========================================
    # نتیجه

    print("\n")
    print("=" * 50)
    print("فاکتور با موفقیت ساخته شد")
    print(output_pdf)
    print("=" * 50)

    return output_pdf


# اضافه کنید به services/invoice_service.py
def create_invoice_from_gui(customer_data, items, invoice_number, invoice_date=None):
    """
    customer_data: dict شامل customer_name, customer_phone, ... (همان ساختار)
    items: list of dict با کلیدهای code, name, qty, price
    invoice_number: str
    invoice_date: str (اختیاری) تاریخ شمسی به فرمت YYYY/MM/DD، اگر None باشد از تاریخ امروز استفاده می‌شود.
    """
    from core.calculator import calculate_total, calculate_tax, calculate_final
    from core.invoice_generator import render_html, save_html, generate_pdf
    from database.customer_repo import save_customer, get_customer_by_phone
    from database.invoice_repo import save_invoice, save_invoice_item
    from config.settings import TAX_RATE, COMPANY_NAME, COMPANY_PHONE, COMPANY_ADDRESS, TEMPLATE_DIR, OUTPUT_HTML_DIR, OUTPUT_PDF_DIR, WKHTMLTOPDF_PATH
    import os, jdatetime

    fixed_data = {
        "company_name": COMPANY_NAME,
        "company_phone": COMPANY_PHONE,
        "company_address": COMPANY_ADDRESS
    }
    # جستجوی مشتری با تلفن
    customer = get_customer_by_phone(customer_data["customer_phone"])
    if customer:
        customer_id = customer[0]
        # به روز رسانی اطلاعات مشتری (اختیاری - می‌توانید update بنویسید)
        # فعلاً از مشتری موجود استفاده می‌کنیم
    else:
        customer_id = save_customer(customer_data)
    # محاسبات
    total_price = calculate_total(items)
    tax = calculate_tax(total_price, TAX_RATE)
    final_price = calculate_final(total_price, tax)
    # تاریخ: اگر از پارامتر داده شده استفاده کن، در غیر این صورت امروز
    if invoice_date is None:
        invoice_date = jdatetime.date.today().strftime("%Y/%m/%d")
    invoice_data = {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "customer_id": customer_id,
        "total_price": total_price,
        "tax": tax,
        "final_price": final_price
    }
    invoice_id = save_invoice(invoice_data)

    for item in items:
        save_invoice_item(invoice_id, item)
    context = {
        **fixed_data,
        **customer_data,
        "invoice_date": invoice_date,
        "items": items,
        "total_price": total_price,
        "tax": tax,
        "final_price": final_price,
    }
    html_content = render_html(TEMPLATE_DIR, "factor_1.html", context)
    output_html = os.path.join(OUTPUT_HTML_DIR, f"invoice_{invoice_id}.html")
    save_html(html_content, output_html)
    output_pdf = os.path.join(OUTPUT_PDF_DIR, f"invoice_{invoice_id}.pdf")
    generate_pdf(output_html, output_pdf, WKHTMLTOPDF_PATH)
    return output_pdf

def regenerate_pdf(invoice_id):
    from database.invoice_repo import get_invoice_by_id, get_invoice_items
    from database.customer_repo import get_customer_by_id
    from core.invoice_generator import render_html, save_html, generate_pdf
    from config.settings import TEMPLATE_DIR, OUTPUT_HTML_DIR, OUTPUT_PDF_DIR, WKHTMLTOPDF_PATH, COMPANY_NAME, COMPANY_PHONE, COMPANY_ADDRESS
    import os, jdatetime

    invoice = get_invoice_by_id(invoice_id)
    if not invoice:
        raise ValueError("فاکتور یافت نشد")
    # invoice: (id, invoice_number, invoice_date, customer_id, total_price, tax, final_price)
    customer = get_customer_by_id(invoice[3])
    # ساخت context مشابه
    fixed_data = {
        "company_name": COMPANY_NAME,
        "company_phone": COMPANY_PHONE,
        "company_address": COMPANY_ADDRESS
    }
    customer_data = {
        "customer_name": customer[1],
        "customer_phone": customer[2],
        "customer_national_code": customer[3],
        "customer_economic_code": customer[4],
        "customer_postal_code": customer[5],
        "customer_address": customer[6],
        "invoice_number": invoice[1]
    }
    items = get_invoice_items(invoice_id)
    # تبدیل آیتم‌ها به فرمت مورد نیاز (با کلیدهای code, name, qty, price)
    items_list = []
    for item in items:
        # item: (id, invoice_id, product_code, product_name, qty, price, total)
        items_list.append({
            "code": item[2],
            "name": item[3],
            "qty": item[4],
            "price": item[5]
        })
    context = {
        **fixed_data,
        **customer_data,
        "invoice_date": invoice[2],
        "items": items_list,
        "total_price": invoice[4],
        "tax": invoice[5],
        "final_price": invoice[6],
    }
    
    html_content = render_html(TEMPLATE_DIR, "factor_1.html", context)
    # ساخت نام فایل یکتا با زمان شمسی
    now = jdatetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    output_html = os.path.join(OUTPUT_HTML_DIR, f"invoice_{invoice_id}_{timestamp}.html")
    save_html(html_content, output_html)
    output_pdf = os.path.join(OUTPUT_PDF_DIR, f"invoice_{invoice_id}_{timestamp}.pdf")
    generate_pdf(output_html, output_pdf, WKHTMLTOPDF_PATH)