

from django.http import JsonResponse

class RespuestaJson:
    """
    Clase para generar respuestas estándar en JSON cuando se requiera.
    """
    def __init__(self, estado: str = 'OK', mensaje: str = '', datos=None):
        self.__estado: str = estado
        self.__mensaje: str = mensaje
        self.__datos = datos

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value: str):
        self.__estado = value

    @property
    def mensaje(self):
        return self.__mensaje

    @mensaje.setter
    def mensaje(self, value: str):
        self.__mensaje = value

    @estado.setter
    def estado(self, value: str):
        self.__estado = value

    @property
    def datos(self):
        return self.__datos

    @datos.setter
    def datos(self, value: str):
        self.__mensaje = value

    def get_jsonresponse(self) -> JsonResponse:
        return JsonResponse({'estado': self.__estado, 'mensaje': self.__mensaje, 'datos': self.__datos})

    @staticmethod
    def exitosa(datos=None, mensaje: str = '') -> JsonResponse:
        """
        Genera una respuesta JSON estándar que indica que fue exitosa.
        :param datos: Datos a adjuntar a la respuesta, debe poderse convertir a JSON.
        :param mensaje: Mensaje de exitoso a enviar.
        :return: JsonResponse con el JSON estándar exitoso. {"estado": "OK", "mensaje": "", "datos": ""}.
        """
        return RespuestaJson(datos=datos, mensaje=mensaje).get_jsonresponse()

    @staticmethod
    def error(mensaje: str = '') -> JsonResponse:
        """
        Genera una respuesta JSON estándar que indica se presentó un error.
        :param mensaje: Descripción del error a enviar.
        :return: JsonResponse con el JSON estándar de error. exitoso {"estado": "error", "mensaje": "", "datos": null}.
        """
        return RespuestaJson(estado="error", mensaje=mensaje).get_jsonresponse()
