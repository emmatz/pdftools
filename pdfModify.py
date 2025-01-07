def uno():
    from pypdf import PdfReader, PdfWriter

    def resize_pdf_page(input_pdf, output_pdf, page_number, scale_factor=None, new_width=None, new_height=None):
        """
        Redimensiona una página específica en un archivo PDF.

        Args:
            input_pdf (str): Ruta al archivo PDF de entrada.
            output_pdf (str): Ruta al archivo PDF de salida.
            page_number (int): Número de página a redimensionar (basado en 0-index).
            scale_factor (float): Factor de escalado. Por ejemplo, 2.0 duplica el tamaño, 0.5 lo reduce a la mitad.
            new_width (float): Nueva anchura en puntos (opcional si scale_factor está presente).
            new_height (float): Nueva altura en puntos (opcional si scale_factor está presente).

        """
        # Cargar el archivo PDF
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Iterar por las páginas del PDF
        for i, page in enumerate(reader.pages):
            if i == page_number:
                # Redimensionar la página
                if scale_factor:
                    page.scale_by(scale_factor)  # Escalar por un factor
                elif new_width and new_height:
                    page.scale_to(new_width, new_height)  # Redimensionar a dimensiones específicas
                else:
                    raise ValueError("Debes proporcionar scale_factor o new_width y new_height.")

            # Agregar la página al PDF final
            writer.add_page(page)

        # Guardar el nuevo PDF
        with open(output_pdf, "wb") as f:
            writer.write(f)

    # Ejemplo de uso
    resize_pdf_page(
        input_pdf=r"..\tmp\copycopy.pdf",
        output_pdf=r"..\tmp\nvofile.pdf",
        page_number=0,        # Primera página (0-index)
        # scale_factor=1.5      # Escala 1.5x
        new_width=842,       # Alternativamente, especificar tamaño en puntos
        new_height=596
    )

def dos():
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject

    # Mediabox:
    #   > Define el área total de la página, incluyendo todo el contenido visible e invisible.
    #   > Es la caja más grande y representa las dimensiones del documento.
    #
    # Cropbox:
    #   > Define el área visible de la página.
    #   > Es una subcaja de mediabox. Solo lo que está dentro de cropbox es visible cuando el PDF
    #   se muestra o imprime.
    #
    # Trimbox:
    #   > Especifica los límites de la página después del recorte, generalmente para imprimir.
    #   > Normalmente se usa para ajustar márgenes para la producción.
    #
    # Bleedbox:
    #   > Define el área de sangrado. Se usa cuando el contenido de la página debe extenderse más allá del
    #   borde para garantizar que no haya bordes blancos después del recorte.
    #
    # Artbox:
    #   > Define el área que contiene el contenido visual o el diseño de la página.

    # Mediabox:
    #  > Defines the total area of the page, including all visible and invisible content.
    #  > It is the largest box and represents the dimensions of the document.
    #
    # Cropbox:
    #  > Defines the visible area of the page.
    #  > It is a sub-box of the Mediabox. Only the content within the Cropbox is
    #  visible when the PDF is displayed or printed.
    #
    # Trimbox:
    #  > Specifies the boundaries of the page after trimming, typically for printing.
    #  > It is commonly used to adjust margins for production purposes.
    #
    # Bleedbox:
    #  > Defines the bleed area. It is used when the page content needs to extend beyond
    #  the edge to ensure there are no white borders after trimming.
    #
    # Artbox:
    #  > Defines the area that contains the visual content or layout of the page.

    # Cargar el archivo PDF
    input_pdf = r"..\tmp\nvofile_17.pdf"
    output_pdf = r"..\tmp\nvofile_3.pdf"

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Ajustar las cajas de la primera página
    page = reader.pages[0]  # Seleccionamos la primera página

    # Obtenemos la mediabox (dimensiones actuales de la página)
    mb = page.mediabox
    print(f'Medidas: {mb}\ntop: {mb.top}\nbottom: {mb.bottom}\nleft: {mb.left}\nright: {mb.right}')

    # Redimensionamos la mediabox y las otras cajas (ejemplo: recorte 50 puntos de cada lado)
    # page.mediabox = RectangleObject((mb.left + 50, mb.bottom + 50, mb.right - 50, mb.top - 50))
    page.mediabox = RectangleObject((mb.left, mb.bottom + 596, mb.right, mb.top))
    page.cropbox = RectangleObject((mb.left, mb.bottom + 596, mb.right, mb.top))
    page.trimbox = RectangleObject((mb.left, mb.bottom + 596, mb.right, mb.top))
    page.bleedbox = RectangleObject((mb.left, mb.bottom + 596, mb.right, mb.top))
    page.artbox = RectangleObject((mb.left, mb.bottom + 596, mb.right, mb.top))

    # Guardamos la página ajustada
    writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print("Página ajustada guardada en", output_pdf)

dos()