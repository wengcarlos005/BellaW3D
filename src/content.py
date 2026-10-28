# Conteúdo do site da Bella W3D. Edite aqui e rode: python3 src/build.py

SITE = {
    "name": "Bella W3D",
    "url": "https://bellaw3d.vercel.app",
    "tagline": "Lembrancinhas e presentes personalizados em impressão 3D",
    "description": (
        "Lembrancinhas, presentes e decoração personalizados em impressão 3D para festas, "
        "formaturas, datas especiais e o quarto das crianças. Envio para todo o Brasil."
    ),
    "whatsapp": "5521964876543",
    "whatsapp_display": "(21) 96487-6543",
    "instagram": "https://www.instagram.com/bellaw_3d/",
    "instagram_handle": "@bellaw_3d",
    "shopee": "https://shopee.com.br/bella_w3d",
    "year": 2026,
}

# Ordem = ordem de exibição. "cover" é o produto cuja foto representa a ocasião.
# "short" é o rótulo curto usado nos cartões da página inicial.
OCCASIONS = [
    {"id": "natal", "label": "Natal", "cover": "guardanapo"},
    {"id": "formatura", "label": "Formatura", "cover": "capelo"},
    {"id": "festas", "label": "Festas e brindes", "short": "Festas", "cover": "taca"},
    {"id": "infantil", "label": "Infantil e Montessori", "short": "Infantil", "cover": "balao"},
    {"id": "dia-dos-pais", "label": "Dia dos Pais", "cover": "retrato"},
    {"id": "halloween", "label": "Halloween", "cover": "abobora"},
    {"id": "chaveiros", "label": "Chaveiros", "cover": "gatinho"},
]

# price=None mostra "Preço sob consulta" e troca o botão principal pelo WhatsApp.
# shopee=None usa o link da loja; cole aqui o link do anúncio quando tiver.
# focus=(x, y) define o ponto que o recorte quadrado da foto preserva (0 a 1).
PRODUCTS = [
    {
        "id": "letreiro", "slug": "letreiro-nome-personalizado-infantil",
        "name": "Letreiro de Nome Personalizado Infantil", "price": 19.80,
        "occasions": ["infantil"], "personal": True,
        "short": "A inicial e o nome da criança em um enfeite cheio de afeto.",
        "desc": "A inicial em destaque, acompanhada do nome da criança: um enfeite cheio de afeto "
                "para o quarto, o nicho da estante ou a mesa do aniversário. Feito com o nome que você escolher.",
    },
    {
        "id": "taca", "slug": "kit-5-marcadores-de-taca-com-nome",
        "name": "Kit 5 Marcadores de Taça com Nome", "price": 25.90, "kit": 5,
        "occasions": ["festas"], "personal": True,
        "short": "Cada convidado encontra a sua taça.",
        "desc": "Cada convidado encontra a sua taça: marcadores com nome para casamentos, aniversários, "
                "despedidas e confraternizações. Charmosos na mesa e ótimos para as fotos.",
    },
    {
        "id": "capelo", "slug": "kit-10-chaveiros-capelo-formatura",
        "name": "Kit 10 Chaveiros Capelo de Formatura", "price": 42.00, "kit": 10, "focus": (1, 0.5),
        "occasions": ["formatura", "chaveiros"],
        "short": "Lembrancinha de formatura em formato de capelo.",
        "desc": "Uma lembrancinha que todo formando guarda: chaveiros em formato de capelo para "
                "presentear a turma, a família ou os professores na colação de grau.",
    },
    {
        "id": "balao", "slug": "kit-3-enfeites-balao-para-parede",
        "name": "Kit 3 Enfeites de Balão para Parede", "price": 19.90, "kit": 3,
        "occasions": ["infantil"],
        "short": "Balões delicados para decorar o quarto infantil.",
        "desc": "Enfeites em formato de balão para decorar a parede do quarto infantil, a brinquedoteca "
                "ou o cantinho da festa. Delicados e cheios de cor, deixam qualquer espaço mais alegre.",
    },
    {
        "id": "retrato", "slug": "kit-2-porta-retratos-dad",
        "name": "Kit 2 Porta-Retratos Dad", "price": 25.90, "kit": 2,
        "occasions": ["dia-dos-pais"],
        "short": "Porta-retrato com a palavra Dad em destaque.",
        "desc": "Porta-retrato com a palavra Dad em destaque, para guardar aquela foto especial com o pai. "
                "Um presente criativo para o Dia dos Pais ou para qualquer data.",
    },
    {
        "id": "guardanapo", "slug": "kit-10-porta-guardanapos-arvore-de-natal",
        "name": "Kit 10 Porta-Guardanapos Árvore de Natal", "price": 29.90, "kit": 10,
        "occasions": ["natal"],
        "short": "Porta-guardanapos de árvore para a mesa da ceia.",
        "desc": "Porta-guardanapos em formato de árvore para deixar a mesa da ceia mais charmosa. "
                "Uma decoração simples que faz diferença no Natal.",
    },
    {
        "id": "etiquetas", "slug": "kit-5-etiquetas-personalizadas-com-nome",
        "name": "Kit 5 Etiquetas Personalizadas com Nome", "price": 24.90, "kit": 5, "focus": (1, 0.5),
        "occasions": ["festas"], "personal": True,
        "short": "Etiquetas com nome para sacolinhas e presentes.",
        "desc": "Etiquetas com o nome que você escolher para dar um toque especial a sacolinhas de "
                "lembrancinha, presentes e embalagens. Ideais para aniversários, chás e festas infantis.",
    },
    {
        "id": "numeros", "slug": "kit-5-numeros-comemorativos-para-mesa",
        "name": "Kit 5 Números Comemorativos para Mesa", "price": None, "kit": 5,
        "occasions": ["festas"],
        "short": "Números decorativos para aniversários e bodas.",
        "desc": "Números decorativos para enfeitar a mesa de aniversários e bodas: 20, 30, 40 anos e mais. "
                "Uma forma elegante de celebrar a idade ou os anos de história juntos. "
                "Consulte números e cores disponíveis pelo WhatsApp.",
    },
    {
        "id": "abobora", "slug": "kit-3-mini-baldes-de-abobora",
        "name": "Kit 3 Mini Baldes de Abóbora", "price": 29.90, "kit": 3,
        "occasions": ["halloween"],
        "short": "Baldinhos de abóbora com alça para doces.",
        "desc": "Mini baldes de abóbora com alça para servir doces, decorar a mesa e entrar no clima do "
                "Halloween. Cada um tem uma carinha diferente.",
    },
    {
        "id": "teia", "slug": "kit-5-porta-copos-teia-de-aranha",
        "name": "Kit 5 Porta-Copos Teia de Aranha", "price": 23.90, "kit": 5,
        "occasions": ["halloween"],
        "short": "Porta-copos temáticos para a mesa de Halloween.",
        "desc": "Porta-copos em formato de teia de aranha para deixar a mesa de Halloween temática. "
                "Divertidos no dia a dia também.",
    },
    {
        "id": "gatinho", "slug": "chaveiro-gatinho-preto",
        "name": "Chaveiro Gatinho Preto", "price": 19.90,
        "occasions": ["chaveiros"],
        "short": "Gatinho preto de orelhinhas rosadas.",
        "desc": "Gatinho preto de orelhinhas rosadas para acompanhar suas chaves, a mochila ou a bolsa. "
                "Um mimo fofo para presentear ou para se dar de presente.",
    },
    {
        "id": "letra", "slug": "chaveiro-letra-personalizada-pai",
        "name": "Chaveiro Letra Personalizada Pai", "price": 19.90,
        "occasions": ["dia-dos-pais", "chaveiros"], "personal": True,
        "short": "A inicial e a palavra pai em um chaveiro.",
        "desc": "Chaveiro com a inicial e a palavra pai: um presente pequeno e cheio de significado para o "
                "Dia dos Pais, para o aniversário ou só para dizer que ele é especial.",
    },
    {
        "id": "galaxia", "slug": "chaveiro-melhor-pai-da-galaxia",
        "name": "Chaveiro Melhor Pai da Galáxia", "price": 19.90,
        "occasions": ["dia-dos-pais", "chaveiros"],
        "short": "Para o pai fã de ficção científica.",
        "desc": "Chaveiro com a frase Best Dad in the Galaxy para o pai fã de ficção científica. "
                "Divertido, criativo e perfeito para o Dia dos Pais.",
    },
    {
        "id": "elefante", "slug": "quebra-cabeca-elefante-montessori",
        "name": "Quebra-Cabeça de Elefante Montessori", "price": 19.30,
        "occasions": ["infantil"],
        "short": "Peças grandes e formas simples de encaixar.",
        "desc": "Quebra-cabeça de elefante inspirado no método Montessori, com peças grandes e formas "
                "simples de encaixar. Para montar, desmontar e brincar de novo.",
    },
    {
        "id": "sorter", "slug": "brinquedo-de-encaixe-montessori",
        "name": "Brinquedo de Encaixe Montessori", "price": 29.90,
        "occasions": ["infantil"],
        "short": "Pinos coloridos para combinar com a base.",
        "desc": "Brinquedo de encaixe inspirado no método Montessori: pinos coloridos para combinar com os "
                "furos da base, explorando cores e tamanhos.",
    },
    {
        "id": "sensorial", "slug": "brinquedo-sensorial-montessori",
        "name": "Brinquedo Sensorial Montessori", "price": 29.90, "focus": (0, 0.5),
        "occasions": ["infantil"],
        "short": "Texturas para explorar com as pontas dos dedos.",
        "desc": "Brinquedo sensorial inspirado no método Montessori, com peças de texturas diferentes para "
                "a criança explorar com as pontas dos dedos e encontrar os pares.",
    },
    {
        "id": "hama", "slug": "chaveiros-pixel-art-personalizados",
        "name": "Chaveiros Pixel Art Personalizados", "price": 24.90,
        "occasions": ["chaveiros"], "personal": True, "material": "Feito com Hama Beads",
        "short": "Pixel art com o desenho que você quiser.",
        "desc": "Chaveiros em pixel art feitos com Hama Beads, com o desenho, a letra ou o tema que você "
                "quiser. Um presente divertido para quem ama games.",
    },
]

# Destaques evitam repetir as fotos de capa das ocasiões.
FEATURED = ["letreiro", "hama", "gatinho", "elefante", "galaxia", "sorter", "letra", "teia"]
# Cada lista é um espaço da colagem do topo; as fotos se alternam sozinhas.
HERO = [["taca", "letreiro", "hama"], ["balao", "abobora", "retrato"], ["gatinho", "capelo", "guardanapo"]]

FAQ = [
    ("Como faço para comprar?",
     "Você pode comprar direto pela nossa loja na Shopee, com pagamento e entrega protegidos pela "
     "plataforma. Se preferir, chame a gente no WhatsApp para tirar dúvidas ou fazer um pedido personalizado."),
    ("Vocês enviam para todo o Brasil?",
     "Sim, enviamos para todo o Brasil. O valor e o prazo do frete aparecem na Shopee de acordo com o seu CEP."),
    ("Posso personalizar as peças?",
     "Muitas peças podem levar nome, tema ou cores escolhidos por você. Conte sua ideia pelo WhatsApp "
     "e a gente verifica o que dá para fazer."),
    ("Qual é o prazo de produção?",
     "As peças são feitas sob encomenda, então o prazo varia conforme o modelo e a quantidade. "
     "Confira no anúncio da Shopee ou pergunte pelo WhatsApp antes de comprar."),
    ("E para festas e eventos com muitos convidados?",
     "Chame a gente no WhatsApp com a quantidade, o tema e a data do evento para conversarmos sobre o seu pedido."),
]
