/**
 * Gerenciador de Anexos
 * 
 * Este script lida com o preview de novos arquivos selecionados (usando DataTransfer)
 * e com a exclusão de anexos existentes via AJAX.
 */

function inicializarGerenciadorAnexos(inputSelector, listaSelector) {
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
            li.textContent = arquivo.name;

            const btnRemover = document.createElement('button');
            btnRemover.textContent = 'Remover';
            btnRemover.type = 'button';
            btnRemover.addEventListener('click', function () {
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
