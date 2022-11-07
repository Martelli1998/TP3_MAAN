import unittest
from yahoo_finance_plotter import *
lista_dias = [1601559000, 1601645400, 1601904600, 1601991000, 1602077400]
Lista_precios_1 = [10,20,30,40,50] # probamos que sucede cuando no hay rendimientos negativos
Lista_precios_2 = [100,90,80,70,60] # probamos que sucede cuando no hay rendimientos negativos
lista_precios_3 = [10,10,10,10,10] #que pasa si son todos iguales
rendimientos_1 = calculo_rendimiento(Lista_precios_1,lista_dias)
rendimientos_2 = calculo_rendimiento(Lista_precios_2,lista_dias)
rendimientos_3 = calculo_rendimiento(lista_precios_3,lista_dias)

class TestSimilares(unittest.TestCase):

	def test_periodo_maximo_rendimiento(self):
		self.assertEqual(periodo_maxima_cantidad_dias_positivos(rendimientos_1,lista_dias),[1.0, 0.5, 0.33333333333333326, 0.25])
		self.assertEqual(periodo_maxima_cantidad_dias_positivos(rendimientos_2,lista_dias),[])
		

	def test_periodo_minimo_rendimiento(self):
		self.assertEqual(Periodo_maxima_cantidad_dias_negativos(rendimientos_1,lista_dias),[])
		self.assertEqual(Periodo_maxima_cantidad_dias_negativos(rendimientos_2,lista_dias),[-0.099,-0.111,-0.125,-0.1428])
		self.assertEqual(Periodo_maxima_cantidad_dias_negativos(rendimientos_3,lista_dias),[10])
	

	def test_maximo_rendimiento(self):
		self.assertEqual(maximo_rendimiento(Lista_precios_1,lista_dias),'300.0%')	
		self.assertEqual(maximo_rendimiento(Lista_precios_2,lista_dias),'-10.0%')
		self.assertEqual(maximo_rendimiento(lista_precios_3,lista_dias),'0.0%')
	

	def test_minimo_rendimiento(self):
		self.assertEqual(minimo_rendimiento(Lista_precios_1,lista_dias),'33.33%')	
		self.assertEqual(minimo_rendimiento(Lista_precios_2,lista_dias),'-30.0%')
		self.assertEqual(minimo_rendimiento(lista_precios_3,lista_dias),'0.0%')

if __name__ == '__main__':
	unittest.main()
