<!DOCTYPE html>
<html>
<head>
    <title>Category Tree</title>
    <style>
        body{font:14px system-ui,sans-serif;margin:24px}
        .action-row{display:flex;align-items:center;gap:8px;margin-bottom:12px}
        .action-row input,.action-row button{font:inherit;padding:7px 9px}
        .category-dropdown{position:relative;width:300px}
        .category-dropdown-btn{width:100%;padding:7px 9px;background:#fff;border:1px solid #999;text-align:left;display:flex;justify-content:space-between;cursor:pointer}
        .category-dropdown-menu{display:none;position:absolute;top:100%;left:0;width:100%;max-height:400px;overflow-y:auto;background:#fff;border:1px solid #999;z-index:10}
        .category-dropdown.open .category-dropdown-menu{display:block}
        .dropdown-tree,.dropdown-tree-children{list-style:none;margin:0;padding:0}
        .dropdown-tree-children{display:none;padding-left:20px}
        .dropdown-tree-children.open{display:block}
        .dropdown-tree-row{display:flex;align-items:center}
        .tree-toggle{width:25px;border:0;background:none;cursor:pointer}
        .tree-spacer{width:25px}
        .category-option{flex:1;padding:7px;cursor:pointer}
        .category-option:hover{background:#e8f1ff}
        #item-name{width:250px;box-sizing:border-box}
        #submit-btn{cursor:pointer}
        #action-status{color:#b42318}
        #selected-info{margin:8px 0 16px;color:#555}
        .tree-root,.tree-children{list-style:none;margin:0;padding-left:20px}
        .tree-root{padding-left:0}
        .tree-node{display:inline-block;padding:3px 8px;cursor:pointer}
        .tree-node:hover{background:#f2f2f2}
        .tree-node.selected{background:#e8f1ff}
        .empty-tree{color:#777}

        details > summary{
            cursor:pointer;
            list-style:none;
        }

        details > summary::-webkit-details-marker{
            display:none;
        }

        .dropdown-tree-node{
            display:inline-block;
            padding:7px;
            cursor:pointer;
        }

        .dropdown-tree-node:hover{
            background:#e8f1ff;
        }
    </style>
</head>

<body>
    <h1>Category Tree</h1>

    <form id="action-form">
        {% csrf_token %}

        <div class="action-row">
            <div class="category-dropdown" id="category-dropdown">
                <button
                    type="button"
                    class="category-dropdown-btn"
                    id="category-dropdown-btn"
                >
                    <span id="category-dropdown-text">
                        Please Select here
                    </span>
                    <span>▼</span>
                </button>

                <div class="category-dropdown-menu">
                    <ul class="dropdown-tree">
                        {% for category in categories %}
                            {% include "dropdown.html" with node=category %}
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <input type="hidden" id="selected-id">
            <input type="hidden" id="selected-type">

            <input
                id="item-name"
                type="text"
                placeholder="Enter name"
            >

            <button type="submit" id="submit-btn">
                ok
            </button>
        </div>

        <p id="selected-info"></p>
        <p id="action-status"></p>

        <ul class="tree-root">
            {% for category in categories %}
                {% include "node.html" with node=category %}
            {% empty %}
                <li class="empty-tree">
                    No categories found
                </li>
            {% endfor %}
        </ul>

        {% if uncategorized_products %}
            <ul class="tree-root">
                {% for prod in uncategorized_products %}
                    {% include "product_node.html" with prod=prod %}
                {% endfor %}
            </ul>
        {% endif %}
    </form>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var form = document.getElementById('action-form');
            var nameInput = document.getElementById('item-name');
            var status = document.getElementById('action-status');

            var dropdown = document.getElementById('category-dropdown');
            var dropdownBtn = document.getElementById('category-dropdown-btn');
            var dropdownText = document.getElementById('category-dropdown-text');

            var selectedId = document.getElementById('selected-id');
            var selectedType = document.getElementById('selected-type');
            var selectedInfo = document.getElementById('selected-info');
            var submitBtn = document.getElementById('submit-btn');

            var selectedNode = null;

            function selectNode(node) {
                var id = node.dataset.id;
                var type = node.dataset.type;
                var name = node.dataset.name;

                if (!name) {
                    name = node.textContent.trim();
                }

                selectedNode = {
                    id: id,
                    type: type,
                    name: name
                };

                selectedId.value = id;
                selectedType.value = type;

                dropdownText.textContent = name;

                selectedInfo.textContent =
                    'Selected ' + type + ': ' + name;

                nameInput.value = '';

                submitBtn.textContent = 'ok';

                status.textContent = '';

                if (node.classList.contains('tree-node')) {
                    document
                        .querySelectorAll('.tree-node.selected')
                        .forEach(function(item) {
                            item.classList.remove('selected');
                        });

                    node.classList.add('selected');
                }

                dropdown.classList.remove('open');
            }

            dropdownBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                dropdown.classList.toggle('open');
            });

            /*
             * Dropdown tree arrows
             */
            dropdown.addEventListener('click', function(e) {
                var toggle = e.target.closest('.tree-toggle');

                if (toggle) {
                    e.preventDefault();
                    e.stopPropagation();

                    var li = toggle.closest('li');

                    if (!li) {
                        return;
                    }

                    var children = li.querySelector(
                        ':scope > .dropdown-tree-children'
                    );

                    if (!children) {
                        return;
                    }

                    var isOpen = children.classList.toggle('open');

                    toggle.textContent = isOpen ? '▼' : '▶';

                    toggle.setAttribute(
                        'aria-expanded',
                        isOpen ? 'true' : 'false'
                    );

                    return;
                }

                /*
                 * Dropdown category/product selection
                 */
                var option = e.target.closest(
                    '.dropdown-tree-node, .category-option'
                );

                if (option) {
                    e.preventDefault();
                    e.stopPropagation();

                    selectNode(option);
                }
            });

            /*
             * Main tree selection
             */
            document.addEventListener('click', function(e) {
                var node = e.target.closest('.tree-node');

                if (!node) {
                    return;
                }

                if (dropdown.contains(node)) {
                    return;
                }

                selectNode(node);
            });

            /*
             * Main tree expansion.
             *
             * Your node.html/product_node.html use <details>,
             * so the browser handles expansion automatically.
             * This code only prevents the selection click from
             * interfering with the <summary>.
             */
            document.addEventListener('click', function(e) {
                var summary = e.target.closest(
                    'summary.dropdown-tree-node'
                );

                if (!summary) {
                    return;
                }

                if (dropdown.contains(summary)) {
                    return;
                }

                selectNode(summary);
            });

            /*
             * Close dropdown when clicking outside
             */
            document.addEventListener('click', function(e) {
                if (!dropdown.contains(e.target)) {
                    dropdown.classList.remove('open');
                }
            });

            /*
             * Database update
             */
            function sendDatabaseUpdate(url, payload) {
                var csrf = document.querySelector(
                    '[name=csrfmiddlewaretoken]'
                ).value;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf
                    },
                    body: JSON.stringify(payload)
                })
                .then(function(response) {
                    if (!response.ok) {
                        return response.text().then(function(message) {
                            throw new Error(
                                message || 'Request failed.'
                            );
                        });
                    }

                    location.reload();
                })
                .catch(function(error) {
                    status.textContent =
                        'Could not save: ' + error.message;
                });
            }

            /*
             * Form submit
             */
            form.addEventListener('submit', function(e) {
                e.preventDefault();

                status.textContent = '';

                var name = nameInput.value.trim();

                if (!selectedNode) {
                    status.textContent =
                        'Select a category or product.';
                    return;
                }

                if (!name) {
                    status.textContent = 'Enter a name.';
                    nameInput.focus();
                    return;
                }

                var endpoint;
                var payload;

                if (selectedNode.type === 'category') {
                    endpoint = '/api/categories/';

                    payload = {
                        action: 'create_sub',
                        parent_id: selectedNode.id,
                        name: name
                    };
                } else if (selectedNode.type === 'product') {
                    endpoint = '/api/product/';

                    payload = {
                        action: 'create_sub_product',
                        parent_product_id: selectedNode.id,
                        name: name
                    };
                } else {
                    status.textContent = 'Invalid selection.';
                    return;
                }

                sendDatabaseUpdate(endpoint, payload);
            });
        });
    </script>
</body>
</html>
