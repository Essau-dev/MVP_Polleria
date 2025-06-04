from PIL import Image
import os

# Configuración
INPUT_LOGO_PATH = 'app/static/img/logo.png' # Asegúrate de que esta ruta sea correcta para tu logo original
OUTPUT_DIR = 'app/static/img/'
SIZES = [
    (192, 192),
    (512, 512),
    # Puedes añadir más tamaños si los necesitas para otros usos
    #(168, 168),
    #(144, 144),
    #(96, 96),
    #(72, 72),
    #(48, 48),
]

def resize_logo(input_path, output_dir, sizes):
    """
    Redimensiona una imagen a múltiples tamaños y los guarda en un directorio.
    """
    if not os.path.exists(input_path):
        print(f"Error: El archivo de entrada no se encontró en {input_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directorio de salida creado: {output_dir}")

    try:
        img = Image.open(input_path)
        print(f"Imagen de entrada cargada: {input_path}")

        # Convertir a RGBA si no lo está para manejar transparencia si existe
        img = img.convert("RGBA")

        for size in sizes:
            width, height = size
            output_filename = f"logo-{width}x{height}.png"
            output_path = os.path.join(output_dir, output_filename)

            print(f"Redimensionando a {width}x{height}...")
            # Usar Image.Resampling.LANCZOS para mejor calidad al reducir
            resized_img = img.resize(size, Image.Resampling.LANCZOS)

            resized_img.save(output_path, 'PNG')
            print(f"Guardado: {output_path}")

        print("Proceso de redimensionamiento completado.")

    except FileNotFoundError:
        print(f"Error: El archivo de entrada no se encontró en {input_path}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    resize_logo(INPUT_LOGO_PATH, OUTPUT_DIR, SIZES)