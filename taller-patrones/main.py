import time
from abc import ABC, abstractmethod

# Base Filter class
class Filter(ABC):
    @abstractmethod
    def process(self, texto: str) -> str:
        pass

# Aspect (decorador) para registrar tiempo de ejecución y operación
def registrar_bitacora(func):
    def wrapper(*args, **kwargs):
        print(func)
        start_time = time.time()  # Start timer
        resultado = func(*args, **kwargs)
        end_time = time.time()    # End timer
        duration = (end_time - start_time) * 1000  # Duration in milliseconds
        print(f"Filtro: {func.__name__}, Tiempo: {duration:.4f} ms")  # Log operation
        return resultado
    return wrapper

# Filters
class IniciarMayuscula(Filter):
    @registrar_bitacora
    def process(self, texto: str) -> str:
        sentences = texto.split('. ')
        sentences = [s.capitalize() for s in sentences]
        return '. '.join(sentences)

class EliminarRepeticiones(Filter):
    @registrar_bitacora
    def process(self, texto: str) -> str:
        words = texto.split()
        filtered_words = [words[0]]
        for word in words[1:]:
            if word != filtered_words[-1]:
                filtered_words.append(word)
        return ' '.join(filtered_words)

class AdicionarFirma(Filter):
    def __init__(self, texto_firma: str):
        self.texto_firma = texto_firma

    @registrar_bitacora
    def process(self, texto: str) -> str:
        return f"{texto}\n\n{self.texto_firma}"

class CorregirOrtografia(Filter):
    @registrar_bitacora
    def process(self, texto: str) -> str:
        palabras = {
            "testo": "texto",
            "patrrones": "patrones",
            "Paipe": "Pipe",
        }

        for palabra, correccion in palabras.items():
            texto = texto.replace(palabra, correccion)
        
        return texto

# Pipe class to handle the filters
class Pipe:
    def __init__(self):
        self.filters = []

    def add_filter(self, filter: Filter):
        self.filters.append(filter)

    def execute(self, texto: str) -> str:
        resultado = texto
        for filter in self.filters:
            resultado = filter.process(resultado)
        return resultado

def leer_texto_desde_archivo(ruta_archivo: str) -> str:
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: El archivo {ruta_archivo} no se encontró.")
        return ""

# Main execution
if __name__ == "__main__":
    ruta_archivo = './data/texto_prueba.txt'

    # Read the text from the file
    texto_inicial = leer_texto_desde_archivo(ruta_archivo)

    # Create the pipe and add filters
    pipe = Pipe()
    pipe.add_filter(IniciarMayuscula())
    pipe.add_filter(EliminarRepeticiones())
    pipe.add_filter(CorregirOrtografia())
    pipe.add_filter(AdicionarFirma("Saludos, Camilo Sotelo"))

    # Execute the pipeline
    resultado = pipe.execute(texto_inicial)

    # Output the processed text
    print("\nTexto procesado:")
    print(resultado)
