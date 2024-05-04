from abc import ABC, abstractmethod
import os
import prodamuspy
from starlette.datastructures import FormData

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class ProdamusVerification:
    @staticmethod
    def verify(form: FormData, verification_code: str):
        if not verification_code:
            return False

        prodamus = prodamuspy.ProdamusPy(os.getenv('PRODAMUS_API_KEY'))

        data = form._dict

        name, price, quantity, summ = data['products[0][name]'], data['products[0][price]'], \
            data['products[0][quantity]'], data['products[0][sum]']
        del data['products[0][name]'], data['products[0][price]'], \
            data['products[0][quantity]'], data['products[0][sum]']
        data["products"] = [
            {
                "name": name,
                "price": price,
                "quantity": quantity,
                "sum": summ,
            }
        ]

        success = prodamus.verify(obj=data, sign=str(verification_code))

        return success