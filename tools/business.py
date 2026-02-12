from __future__ import annotations
from typing import Dict, List
from datetime import datetime, timedelta

def calculate_discount(price: float, discount_percent: float, tax_rate: float = 0.0) -> Dict:
    """Calculate final price after discount and tax"""
    discount_amount = price * (discount_percent / 100)
    price_after_discount = price - discount_amount
    tax_amount = price_after_discount * (tax_rate / 100)
    final_price = price_after_discount + tax_amount
    
    return {
        "original_price": price,
        "discount_amount": round(discount_amount, 2),
        "price_no_tax": round(price_after_discount, 2),
        "tax_amount": round(tax_amount, 2),
        "final_price": round(final_price, 2)
    }


def validate_email(email: str) -> Dict:
    """Validate email format and extract domain"""
    import re
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    match = re.match(pattern, email)
    
    if match:
        domain = email.split('@')[1]
        return {"valid": True, "domain": domain}
    return {"valid": False, "error": "Invalid format"}


def generate_invoice(customer: Dict, items: List[Dict]) -> Dict:
    """Generate an invoice structure"""
    total = sum(item['price'] * item['qty'] for item in items)
    return {
        "invoice_id": f"INV-{int(datetime.now().timestamp())}",
        "date": datetime.now().isoformat(),
        "customer": customer,
        "items": items,
        "total": round(total, 2),
        "status": "DRAFT"
    }


def schedule_reminder(task: str, delay_minutes: int) -> str:
    """Schedule a reminder (Mock)"""
    remind_time = datetime.now() + timedelta(minutes=delay_minutes)
    return f"Reminder set for '{task}' at {remind_time.strftime('%H:%M')}"
