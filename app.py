# entrar no site
# realizar login
# pesquisar pelo cargo
# filtrar por pessoas
# encontrar botões "conectar"
# clicar em conectar
# fazer isso para até 20 pessoas
# aguardar 24 horas

import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from time import sleep
from utils import iniciar_contagem_regressiva, rolar_pagina_totalmente_para_baixo, rolar_pagina_totalmente_para_cima

logging.basicConfig(filename='erros.log', filemode='a', level=logging.ERROR)


def conectar_com_pessoas_na_pagina_atual(driver, wait, window):
    limite_diario = 20
    conexoes_enviadas = 0

    try:
        window.write_output("buscando por botões de conectar na página atual\n")
        rolar_pagina_totalmente_para_baixo(driver)
        rolar_pagina_totalmente_para_cima(driver)
    except Exception as error:
        window.write_output("erro ao tentar rolar a página, favor entrar em contato com o suporte\n")
        logging.error(error)

    sleep(random.randint(2,5))
    try:
        botoes_conectar = wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//button[contains(@aria-label, 'Convidar')]")))
        window.write_output("encontrado o botão conectar\n")

        for botao_conectar in botoes_conectar:
            if conexoes_enviadas <= limite_diario:
                sleep(random.randint(2,5))
                driver.execute_script("arguments[0].click()", botao_conectar)
                window.write_output("clicado no botão conectar\n")
                sleep(random.randint(2,5))

                # Extrair nome do contato
                elemento_com_nome_do_contato = wait.until(EC.element_to_be_clickable(((By.XPATH,"//span[@class='flex-1']/strong"))))
                nome = elemento_com_nome_do_contato.text

                # Clicar em enviar sem nota
                botao_enviar_sem_nota = wait.until(EC.element_to_be_clickable(((By.XPATH,"//button[@aria-label='Enviar sem nota']"))))
                window.write_output(f"Enviando convite sem nota para {nome}\n")
                sleep(random.randint(2,5))

                botao_enviar_sem_nota.click()
                window.write_output(f"{nome} acaba de ser convidado!\n")
                conexoes_enviadas += 1

                print(f"Enviado {conexoes_enviadas} de {limite_diario} conexões diárias")
                sleep(random.randint(2,5))
            else:
                # Esperar 24 horas antes de continuar a execução
                sleep(86400)
    
    except Exception as error:
        window.write_output("houve um erro ao tentar encontrar os botões para se conectar com outras pessoas, favor entrar em contato com o suporte\n")
        logging.error(error)


def ir_para_proxima_pagina(driver, wait, window):
    # Verificar se é possível ir para a próxima página
    rolar_pagina_totalmente_para_baixo(driver)
    window.write_output('buscando botão de próxima página\n')

    botao_ir_para_proxima_pagina = wait.until(EC.element_to_be_clickable(((By.XPATH,"//button[@aria-label='Avançar']"))))
    sleep(random.randint(2,5))

    if botao_ir_para_proxima_pagina.is_enable() is True:
        botao_ir_para_proxima_pagina.click()
        window.write_output('indo para a próxima página\n')
        conectar_com_pessoas_na_pagina_atual(driver, wait, window, conexoes_enviadas)
    else:
        window.write_output('automação chegou à última página!\n')
        driver.quit()
        window["iniciar_automacao"].update(disable=False)

def iniciar_driver():
    chrome_options = Options()
    arguments = ["--lang=pt-BR", "--window-size=1920,1080", "--lang=pt-BR"]
    for argument in arguments:
        chrome_options.add_arguments(argument)
    
    chrome_options.add_experimental_options('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )

    return driver, wait

def iniciar_automacao(palavra_chave, window):
    driver, wait = iniciar_driver()

    link_pesquisa_por_palavra_chave = f"https://www.linkedin.com/search/results/people/?keywords={palavra_chave}&origin=SWITCH_SEARCH_VERTICAL&sid=B_%40"

    driver.get(link_pesquisa_por_programadores)
    iniciar_contagem_regressiva(60,1,window)
    conectar_com_pessoas_na_pagina_atual(driver, wait, window)
    ir_para_proxima_pagina(driver, wait, window)
    sleep(random.randint(2,5))
    