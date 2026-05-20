/**
 * Gerenciador de Anexos
 * 
 * Este script lida com o preview de novos arquivos selecionados (usando DataTransfer)
 * e com a exclusão de anexos existentes via AJAX.
 */

function inicializarGerenciadorAnexos(inputSelector, listaSelector, extensoesImagem = [], extensoesVideo = []) {
    const inputAnexos = document.querySelector(inputSelector);
    const listaAnexos = document.querySelector(listaSelector);

    if (!inputAnexos || !listaAnexos) return;

    // DataTransfer permite manipular a FileList do input (nativa do JS)
    let dataTransfer = new DataTransfer();

    inputAnexos.addEventListener('change', function () {
        // Adiciona os novos arquivos ao DataTransfer existente para acumular seleções
        for (const arquivo of this.files) {
            dataTransfer.items.add(arquivo);
        }

        // Atualiza o input com todos os arquivos acumulados
        inputAnexos.files = dataTransfer.files;

        renderizarListaPreview();
    });

    function renderizarListaPreview() {
        listaAnexos.innerHTML = '';

        Array.from(dataTransfer.files).forEach(function (arquivo, indice) {
            const li = document.createElement('li');

            // Renderiza preview conforme o tipo de arquivo
            const previewUrl = URL.createObjectURL(arquivo);

            // Obtém a extensão do arquivo como fallback caso o navegador não detecte o MIME Type (muito comum no Windows)
            const extensao = arquivo.name.split('.').pop().toLowerCase();
            const isImage = arquivo.type.startsWith('image/') || extensoesImagem.includes(extensao);
            const isVideo = arquivo.type.startsWith('video/') || extensoesVideo.includes(extensao);

            if (isImage) {
                const figure = document.createElement('figure');
                const link = document.createElement('a');
                link.href = previewUrl;
                link.target = '_blank';
                const img = document.createElement('img');
                img.src = previewUrl;
                img.alt = arquivo.name;
                img.className = 'anexo-midia';
                img.onerror = function () {
                    lidarErroMidia(img, arquivo.name, previewUrl);
                };
                link.appendChild(img);
                figure.appendChild(link);
                li.appendChild(figure);
            } else if (isVideo) {
                const figure = document.createElement('figure');
                const video = document.createElement('video');
                video.src = previewUrl;
                video.controls = true;
                video.className = 'anexo-midia';
                video.onerror = function () {
                    lidarErroMidia(video, arquivo.name, previewUrl);
                };
                figure.appendChild(video);
                li.appendChild(figure);
            } else {
                li.textContent = arquivo.name;
            }

            const btnRemover = document.createElement('button');
            btnRemover.textContent = 'Remover';
            btnRemover.type = 'button';
            btnRemover.addEventListener('click', function () {
                // Libera a URL de preview para evitar vazamento de memória
                URL.revokeObjectURL(previewUrl);
                // Remove o item do DataTransfer e atualiza o input
                dataTransfer.items.remove(indice);
                inputAnexos.files = dataTransfer.files;
                renderizarListaPreview();
            });

            li.appendChild(document.createTextNode(' '));
            li.appendChild(btnRemover);
            listaAnexos.appendChild(li);
        });
    }
}

/**
 * Função para excluir anexos existentes no servidor via AJAX
 * 
 * @param {string} url - URL para a view de exclusão
 * @param {string} anexoId - ID do elemento li que contém o anexo para remoção visual
 * @param {string} csrftoken - Token CSRF do Django
 */
function excluirAnexoExistente(url, anexoId, csrftoken) {
    if (!confirm('Tem certeza que deseja excluir este anexo definitivamente?')) return;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => {
            if (response.ok) {
                // Se a exclusão no servidor funcionou, removemos o item da lista na tela
                const elemento = document.getElementById(anexoId);
                if (elemento) {
                    const lista = elemento.parentElement;
                    elemento.remove();

                    // Se a lista de anexos atuais ficar vazia, oculta o título e a lista
                    if (lista && lista.children.length === 0) {
                        const titulo = document.getElementById('titulo-anexos-atuais');
                        if (titulo) titulo.style.display = 'none';
                        lista.style.display = 'none';
                    }
                }
            } else {
                alert('Erro ao excluir anexo.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro de comunicação com o servidor.');
        });
}

/**
 * Trata erros de renderização de mídia (imagem/vídeo) exibindo um fallback amigável.
 * 
 * @param {HTMLElement} elemento - O elemento img ou video que falhou.
 * @param {string} nomeArquivo - O nome do arquivo a ser exibido.
 * @param {string} urlArquivo - A URL de download/visualização do arquivo.
 */
function lidarErroMidia(elemento, nomeArquivo, urlArquivo) {
    const container = elemento.closest('figure') || elemento.parentElement;
    if (container) {
        // Evita duplicar a mensagem de erro caso o evento de erro seja disparado múltiplas vezes
        if (container.querySelector('.erro-renderizacao-anexo')) {
            return;
        }

        const divFallback = document.createElement('div');
        divFallback.className = 'erro-renderizacao-anexo';

        const msg = document.createElement('span');
        msg.textContent = 'Não foi possível carregar a pré-visualização deste arquivo.';

        const link = document.createElement('a');
        link.href = urlArquivo;
        link.target = '_blank';
        link.textContent = 'Baixar/Visualizar: ' + nomeArquivo;

        divFallback.appendChild(msg);
        divFallback.appendChild(link);

        container.innerHTML = '';
        container.appendChild(divFallback);
    }
}
