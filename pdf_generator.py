import os
# import pdfkit
import platform
from datetime import datetime

SERVICE_LABELS = {
    "FS_BUILD": "Construction (BuildNet)",
    "FS_SECURE": "Security Guards (SecureForce)",
    "FS_LEGAL": "Legal & GST (Filings)",
    "FS_MEDICAL": "Medical Services",
    "FS_LAND": "Land Verification",
    "FS_REPAIR": "Repair & Maintenance",
    "FS_FINANCE": "Finance Assistant"
}

# Mac aur Windows ke paths
if platform.system() == "Darwin":
    WKHTMLTOPDF_CMD = "/usr/local/bin/wkhtmltopdf"
else:
    WKHTMLTOPDF_CMD = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

# Global config ko None rakhein agar file nahi milti
try:
    if os.path.exists(WKHTMLTOPDF_CMD):
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    else:
        config = None
except Exception:
    config = None

def generate_invoice(customer_info, enquiry_info):
    if config is None:
        return "⚠️ PDF Engine (wkhtmltopdf) not found. Please install it to generate PDFs."

    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("."))
    
    try:
        template = env.get_template("invoice_template.html")
    except Exception:
        return "❌ Error: 'invoice_template.html' not found."

    service_type = enquiry_info.get("service_type")
    context = {
        "customer": customer_info,
        "enquiry": enquiry_info,
        "service_label": SERVICE_LABELS.get(service_type, "FastSewa Service"),
        "generated_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
    }

    html_content = template.render(context)
    output_dir = "generated_pdfs"
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"FastSewa_{service_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = os.path.join(output_dir, file_name)

    pdfkit.from_string(html_content, output_path, configuration=config)
    return f"📄 PDF generated successfully: {output_path}"