# Códigos de Automação para WhatsApp e Organização de Pastas

Este repositório contém diversos códigos em Python para automatização de envio de mensagens no WhatsApp Web e organização de pastas. Abaixo está uma descrição detalhada de cada código, bem como as configurações que você deve ajustar antes de utilizá-los.

## 1. `Enviar_Whatsapp_figurinha.py`
Este código automatiza o envio de figurinhas (stickers) pelo WhatsApp Web, utilizando a biblioteca Selenium para interagir com a interface do WhatsApp Web.

### Instruções de Uso:
- **Alterações Necessárias:** Substitua todas as ocorrências de `SEU_USUARIO` pelo seu nome de usuário do Windows para que o código localize corretamente os arquivos no seu sistema.
- **Pré-requisitos:** Instale as bibliotecas necessárias como `selenium` e configure corretamente o WebDriver do navegador que você estiver utilizando (Chrome ou Firefox).

## 2. `Enviar_Whatsapp_mensagem.py`
Automatiza o envio de mensagens de texto pelo WhatsApp Web usando Selenium.

### Instruções de Uso:
- **Alterações Necessárias:** Substitua todas as ocorrências de `SEU_USUARIO` pelo seu nome de usuário do Windows para que o código localize corretamente os arquivos no seu sistema.
- **Pré-requisitos:** Instale as bibliotecas necessárias como `selenium` e configure corretamente o WebDriver do navegador que você estiver utilizando (Chrome ou Firefox).

## 3. `Enviar_Whatsapp_video_Aleatorio.py`
Este código permite o envio de vídeos aleatórios para contatos no WhatsApp Web. Ele seleciona um vídeo de uma pasta ou lista e realiza o envio.

### Instruções de Uso:
- **Alterações Necessárias:**
Substitua todas as ocorrências de `SEU_USUARIO` pelo seu nome de usuário do Windows para que o código localize corretamente os arquivos no seu sistema.
Defina as variáveis `pasta_nao_enviados` e `pasta_enviados`.
Certifique-se de colocar `\\` (duas barras invertidas) na declaração do caminho, seguindo o exemplo deixado no próprio código.
- **Pré-requisitos:** Instale as bibliotecas necessárias como `selenium` e configure corretamente o WebDriver do navegador que você estiver utilizando (Chrome ou Firefox).

## 4. `Enviar_Whatsapp_video_Especifico.py`
Este código automatiza o envio de um vídeo específico para contatos no WhatsApp Web.

### Instruções de Uso:
- **Alterações Necessárias:** Substitua `SEU_USUARIO` pelo nome de usuário do Windows.
- **Pré-requisitos:** Instale as bibliotecas necessárias como `selenium` e configure corretamente o WebDriver do navegador que você estiver utilizando (Chrome ou Firefox).

## 5. `Organização.py`
Defina as variáveis `source_folder` (origem) e `destination_folder` (destino) para especificar de onde os arquivos serão movidos e para onde serão transferidos.

### Instruções de Uso:
- **Alterações Necessárias:** Ao definir as variáveis de origem e destino, certifique-se de colocar `\\` (duas barras invertidas) na declaração do caminho, seguindo o exemplo deixado no próprio código.
- **Funcionamento:** Ele reorganiza arquivos e pastas dentro do diretório indicado.

## 6. `reordenar_pastas.py`
Código para reordenação de pastas. Ele permite que você altere a ordem das pastas manualmente ou automaticamente, reorganizando o conteúdo da pasta onde o código está localizado.

### Instruções de Uso:
- **Alterações Necessárias:** Nenhuma alteração específica é necessária, exceto rodar o código no diretório onde deseja reorganizar as pastas.
- **Funcionamento:** Ele reorganiza pastas no diretório onde o próprio código está salvo.

---

### Observações Gerais:
- Certifique-se de ter o Python instalado.
- Instale as bibliotecas necessárias rodando:
  ```bash
  pip install selenium
