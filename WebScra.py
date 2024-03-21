import requests
import os
import bs4

def normalize_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    return url

def download_images(soup, url):
    image_links = soup.find_all('img')
    if image_links:
        print("Descargando imágenes...")
        for img in image_links:
            img_url = img.get('src')
            if img_url.startswith('//'):
                img_url = 'http:' + img_url
            elif not img_url.startswith('http'):
                img_url = url + '/' + img_url
            filename = os.path.basename(img_url)
            with open(os.path.join('imágenes', filename), 'wb') as f:
                img_response = requests.get(img_url)
                f.write(img_response.content)

def download_pdfs(soup, url):
    pdf_links = soup.find_all('a', href=lambda href: (href and href.endswith('.pdf')))
    if pdf_links:
        print("Descargando PDFs...")
        for pdf_link in pdf_links:
            pdf_url = pdf_link.get('href')
            if not pdf_url.startswith('http'):
                pdf_url = url + '/' + pdf_url
            filename = os.path.basename(pdf_url)
            with open(os.path.join('PDF', filename), 'wb') as f:
                pdf_response = requests.get(pdf_url)
                f.write(pdf_response.content)

def extract_hyperlinks(soup, url):
    hyperlinks = soup.find_all('a', href=True)
    if hyperlinks:
        print("Extrayendo hipervínculos...")
        with open('hyperlinks.txt', 'w') as f:
            for link in hyperlinks:
                href = link.get('href')
                if not href.startswith('http'):
                    href = url + '/' + href
                f.write(href + '\n')

def main():
    url = input("Ingrese la URL a analizar: ")
    url = normalize_url(url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        
        if not os.path.exists('imágenes'):
            os.makedirs('imágenes')
        if not os.path.exists('PDF'):
            os.makedirs('PDF')
        
        download_images(soup, url)
        download_pdfs(soup, url)
        extract_hyperlinks(soup, url)
        
        print("Se ha guardado con éxito")
        
    except Exception as e:
        print("Ups, ha ocurrido un error:", e)

if __name__ == "__main__":
    main()
