from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from string import ascii_lowercase, ascii_uppercase


def validate_password(value):
	if len(value) < 4:
		raise ValidationError(gettext_lazy("Password must contain more than 4 symbols"), params={"value": value})

	def letters_check(val, all_letters):
		contain = False
		for letter in val:
			if letter not in all_letters:
				continue
			else:
				contain = True
				break
		return contain

	if not letters_check(value, ascii_lowercase):
		raise ValidationError(gettext_lazy("Password must contain lowercase letters"), params={"value": value})
	if not letters_check(value, ascii_uppercase):
		raise ValidationError(gettext_lazy("Password must contain uppercase letters"), params={"value": value})




