from .models import StaffNumber
def release_staff_number(number):
    try:
        staff_number = StaffNumber.objects.get(number=number)
        staff_number.is_in_use = False
        staff_number.save()
        return True
    except StaffNumber.DoesNotExist:
        return False  # Staff number not found