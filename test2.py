from selenium import webdriver
import time


lang_dict = {
 'Deutsch': 'Top 100 Kryptowährungen nach Börsenwert',
 'English': 'Top 100 Cryptocurrencies by Market Capitalization',
 'Español': 'Principales 100 Criptomonedas por capitalización de mercado',
 'Filipino': 'Nangungunang 100 Mga Cryptocurrency ng Market Capitalization',
 'Français': 'Top 100 Crypto-monnaies par capitalisation de marché',
 'हिन्दी': '100 क्रिप्टोकरेंसी बाजार पूंजीकरण के द्वारा टॉप पर',
 'Italiano': 'Migliori 100 Criptovalute per Capitalizzazioni di mercato',
 '日本語': '仮想通貨時価総額上位100',
 '한국어': '시가총액에 의한 최고 100 암호화폐',
 'Português Brasil': 'Top 100 Criptomoedas por Capitalização de Mercado',
 'Русский': 'Топ-100 Криптовалюты по рыночной капитализации',
 'Türkçe': 'Piyasa Değerine Göre , en iyi 100 Kripto Para Birimleri',
 'Tiếng Việt': 'Top 100 Các loại tiền điện tử theo vốn hóa thị trường',
 '简体中文': '市值前100 加密货币', '繁體中文': '市值前 100 加密貨幣'
}

driver = webdriver.Firefox()


def click_language():
    btn_language = driver.find_element_by_class_name("sc-14gaqg0-0")
    btn_language.click()


def find_language_board():
    return driver.find_elements_by_class_name("cmc-language-picker__option")


def test_selenium():

    driver.get('https://coinmarketcap.com')


    click_language()
    language_list = find_language_board()
    click_language()

    for number in range(len(lang_dict)):
        click_language()
        language_list = find_language_board()
        language = language_list[number].text
        language_list[number].click()
        assert lang_dict[language] == driver.find_element_by_tag_name("h1").text, f"Language {language} is incorrect"

    driver.close()
