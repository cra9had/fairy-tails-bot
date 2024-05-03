import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import aiohttp
import prodamuspy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class GeneratePaymentLinkFabric(ABC):
    @abstractmethod
    async def generate_payment_link(self, *args, **kwargs) -> str:
        pass


@dataclass
class GeneratePaymentLinkProdamus(GeneratePaymentLinkFabric):

    prodamus_api_key: str
    prodamus_payment_url: str
    product_name: str

    @staticmethod
    async def _get_request_to_generate_url(url) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()

                return data

    async def generate_payment_link(self, price: int, order_id: int) -> str:
        data = {
            "do": "link",
            "order_id": order_id,
            "products": [
                {
                    "name": self.product_name,
                    "price": price,
                    "quantity": 1,

                }
            ]
        }
        prodamus = prodamuspy.ProdamusPy(self.prodamus_api_key)
        data["sign"] = prodamus.sign(data)

        url_to_request = f"{self.prodamus_payment_url}?order_id={data['order_id']}&products[0][name]={data['products'][0]['name']}" \
              f"&do=link&sign={data['sign']}&sys={data['sign']}&products[0][quantity]={data['products'][0]['quantity']}&products[0][price]={data['products'][0]['price']}"

        payment_url = await self._get_request_to_generate_url(url_to_request)

        return payment_url
