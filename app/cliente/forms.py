from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, validators
from wtforms.validators import InputRequired
import sys
import string

DIVISOR = 11


def first_check_digit(number, weighs):
    """ This function calculates the first check digit to
        verify a cpf or cnpj vality.
        :param number: cpf or cnpj number to check the first
                       digit.  Only numbers.
        :type number: string
        :param weighs: weighs related to first check digit
                       calculation
        :type weighs: list of integers
        :returns: string -- the first digit
    """

    sum = 0
    for i in range(len(weighs)):
        sum = sum + int(number[i]) * weighs[i]
    rest_division = sum % DIVISOR
    if rest_division < 2:
        return '0'
    return str(11 - rest_division)


def second_check_digit(updated_number, weighs):
    """ This function calculates the second check digit to
        verify a cpf or cnpj vality.
        **This function must be called after the above.**
        :param updated_number: cpf or cnpj number with the
                               first digit.  Only numbers.
        :type number: string
        :param weighs: weighs related to second check digit calculation
        :type weighs: list of integers
        :returns: string -- the second digit
    """

    sum = 0
    for i in range(len(weighs)):
        sum = sum + int(updated_number[i]) * weighs[i]
    rest_division = sum % DIVISOR
    if rest_division < 2:
        return '0'
    return str(11 - rest_division)

def clear_punctuation(document):
    """Remove from document all pontuation signals."""
    document = str(document)
    if sys.version_info[0] < 3:
        return document.translate(None, string.punctuation)
    else:
        return document.translate(str.maketrans("", "", string.punctuation))

def validarCpfCnpj(form, field):
    entrada = field.data
    if len(entrada) == 14:
        cnpj = clear_punctuation(entrada)

        firstcnpj_weighs = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        secondcnpj_weighs = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        first_part = cnpj[:12]
        first_digit = cnpj[12]
        second_digit = cnpj[13]

        if not (first_digit == first_check_digit(first_part,firstcnpj_weighs) and
                second_digit == second_check_digit(cnpj[:13],secondcnpj_weighs)):
            raise ValidationError('Cnpj Inválido')

    else:
        if len(entrada) != 11 or not entrada.isdigit():
            raise ValidationError('Cpf Inválido')

        digito = {}
        digito[0] = 0
        digito[1] = 0
        a = 10
        total = 0
        for c in range(0, 2):
            for i in range(0, (8 + c + 1)):
                total = total + int(entrada[i]) * a
                a = a - 1
            digito[c] = int(11 - (total % 11))
            a = 11
            total = 0
        if (int(entrada[9]) == int(digito[0]) and int(entrada[10]) == int(digito[1])):
            for i in (range(len(entrada))):
                if (i == 2 or i == 5):
                    sep = entrada[i] + " ."
                elif (i == 8):
                    sep = entrada[i] + " -"
                else:
                    sep = entrada[i]
        else:
            raise ValidationError('Cpf Inválido')


class ClienteForm(FlaskForm):
    cpfCnpj = StringField('Cpf/Cnpj',[InputRequired(), validarCpfCnpj],_prefix="onkeypress=''")
    nome = StringField('Nome')
    submit = SubmitField('Cadastrar')
