import abc
from typing import List

from App.Models.Sale import Sale


class Shop:


    @classmethod
    @abc.abstractmethod
    def getSales(cls, pages: int = 10, salesGt: int = 1000, discountRateGt: int = 70) -> List[Sale]:
        """
        Lista promoções do determinado site

        Parâmetros:
        pages (int): A quantidade de páginas de promoções a serem analisadas
        salesGt (int): Quantidade minima de vendas para o produto ser considerado.
        discountRateGt (int): Rate mininmo do desconto para o produto ser considerado


        Retorna:
        list[Sale]: a lista de produtos encontrados.
        """
        raise NotImplemented
