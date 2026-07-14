// Tola - SPA Frontend Logic with Multiple Trips Support (Single-User Mode)

let listLocked = false;
let activeTripId = null;
let tripsList = [];

function formatMarkdown(text) {
    if (!text) return '';
    
    // First, escape HTML to prevent XSS
    let escaped = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');

    // Helper to replace inline styles (bold, italics)
    function replaceInline(str) {
        return str
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/__([^_]+)__/g, '<strong>$1</strong>')
            .replace(/\*([^*]+)\*/g, '<em>$1</em>')
            .replace(/_([^_]+)_/g, '<em>$1</em>');
    }

    const lines = escaped.split('\n');
    let formattedHtml = '';
    let inUl = false;
    let inOl = false;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        let trimmed = line.trim();

        // Check for unordered list items (* or - or bullet)
        let ulMatch = line.match(/^(\s*)[\*\-\u2022]\s+(.*)$/);
        // Check for ordered list items (1. 2. etc)
        let olMatch = line.match(/^(\s*)(\d+)\.\s+(.*)$/);

        if (ulMatch) {
            if (inOl) {
                formattedHtml += '</ol>';
                inOl = false;
            }
            if (!inUl) {
                formattedHtml += '<ul>';
                inUl = true;
            }
            formattedHtml += `<li>${replaceInline(ulMatch[2])}</li>`;
        } else if (olMatch) {
            if (inUl) {
                formattedHtml += '</ul>';
                inUl = false;
            }
            if (!inOl) {
                formattedHtml += '<ol>';
                inOl = true;
            }
            formattedHtml += `<li>${replaceInline(olMatch[3])}</li>`;
        } else {
            if (inUl) {
                formattedHtml += '</ul>';
                inUl = false;
            }
            if (inOl) {
                formattedHtml += '</ol>';
                inOl = false;
            }
            if (trimmed) {
                formattedHtml += `<p>${replaceInline(trimmed)}</p>`;
            }
        }
    }

    if (inUl) formattedHtml += '</ul>';
    if (inOl) formattedHtml += '</ol>';

    return formattedHtml;
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    // 1. Load theme
    const savedTheme = localStorage.getItem('tola-theme') || 'sand';
    document.getElementById('themeSelect').value = savedTheme;
    document.documentElement.setAttribute('data-theme', savedTheme);

    // 2. Load trips
    loadTrips();
});

async function changeTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('tola-theme', theme);
    const themeSelect = document.getElementById('themeSelect');
    if (themeSelect) themeSelect.value = theme;

    if (activeTripId) {
        const trip = tripsList.find(t => t.trip_id === activeTripId);
        if (trip && trip.theme !== theme) {
            trip.theme = theme;
            try {
                await fetch(`/api/trips/${activeTripId}/theme`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ theme })
                });
            } catch (e) {
                console.error("Error updating trip theme:", e);
            }
        }
    }
}

async function loadTrips() {
    try {
        const res = await fetch(`/api/trips`);
        if (res.ok) {
            tripsList = await res.json();
            
            if (tripsList.length > 0) {
                if (!activeTripId || !tripsList.find(t => t.trip_id === activeTripId)) {
                    activeTripId = tripsList[0].trip_id;
                }
                
                showDashboardView();
                renderTripSelector();
                selectActiveTripUI();
            } else {
                // If no trips exist, show onboarding view to initialize the first one
                showOnboardingView();
            }
        } else {
            showOnboardingView();
        }
    } catch (err) {
        showOnboardingView();
        showToast("Error connecting to server.", "error");
    }
}

function renderTripSelector() {
    const select = document.getElementById('tripSelect');
    select.innerHTML = '';
    
    tripsList.forEach(t => {
        const opt = document.createElement('option');
        opt.value = t.trip_id;
        opt.innerText = `${t.trip_name} (${t.start_date})${t.is_archived ? ' [Archived]' : ''}`;
        select.appendChild(opt);
    });
    
    select.value = activeTripId;

    // Show manager header
    const mgrHeader = document.getElementById('tripManagerHeader');
    mgrHeader.style.display = 'flex';
}

async function selectActiveTripUI() {
    const trip = tripsList.find(t => t.trip_id === activeTripId);
    if (!trip) return;

    document.getElementById('dashboardTripTitle').innerText = `Checklist for: ${trip.trip_name}`;
    listLocked = trip.list_locked === 1;
    
    const archivedBadge = document.getElementById('archivedBadge');
    if (trip.is_archived === 1) {
        archivedBadge.style.display = 'inline-block';
        document.getElementById('addItemPanel').style.display = 'none';
    } else {
        archivedBadge.style.display = 'none';
        document.getElementById('addItemPanel').style.display = 'block';
    }

    updateLockUI();
    renderPackingList();
    loadCopilotChatHistory(trip.trip_id);

    if (trip.theme) {
        changeTheme(trip.theme);
    }

    document.getElementById('btnToggleLock').style.display = 'inline-block';
}

async function loadCopilotChatHistory(tripId) {
    const container = document.getElementById('copilotChatMessages');
    if (!container) return;
    container.innerHTML = '';
    try {
        const res = await fetch(`/api/copilot/history?trip_id=${tripId}`);
        if (res.ok) {
            const history = await res.json();
            history.forEach(msg => {
                appendCopilotMessage(msg.role, msg.text);
            });
        }
    } catch (err) {
        console.error("Error loading copilot history:", err);
    }
}

function changeActiveTrip(tripId) {
    const normalizedTripId = String(tripId).trim();
    if (!/^[A-Za-z0-9_-]+$/.test(normalizedTripId)) {
        showToast("Invalid trip selected.", "error");
        return;
    }
    activeTripId = normalizedTripId;
    selectActiveTripUI();
}

// Onboarding & Wizard Controls
function showNewTripWizard() {
    document.getElementById('wizardCancelBtnRow').style.display = 'block';
    showOnboardingView();
}

function cancelWizard() {
    if (onboardingChatHistory.length > 1) {
        if (!confirm("Your trip onboarding details are not saved yet. Are you sure you want to leave?")) {
            return;
        }
    }
    if (tripsList.length > 0) {
        showDashboardView();
    }
}

function showOnboardingView() {
    document.getElementById('onboardingView').classList.add('active');
    document.getElementById('dashboardView').classList.remove('active');
    document.getElementById('tripManagerHeader').style.display = 'none';

    // Hide copilot sidebar and make grid full-width
    const sidebar = document.getElementById('copilotSidebar');
    if (sidebar) sidebar.style.display = 'none';
    const grid = document.getElementById('workspaceGrid');
    if (grid) grid.classList.add('onboarding-active');

    // Initialize onboarding chat if empty
    const messagesContainer = document.getElementById('onboardingChatMessages');
    if (messagesContainer && messagesContainer.children.length === 0) {
        onboardingChatHistory = [];
        const greeting = "Hi! I'm Tola, your AI travel companion. Let's set up your new trip! What is your name and where are you planning to travel?";
        appendOnboardingChatMessage("copilot", greeting);
        onboardingChatHistory.push({ role: "copilot", text: greeting });
    }

    // Push history state to intercept browser "back" navigation
    if (!history.state || history.state.page !== 'onboarding') {
        history.pushState({ page: 'onboarding' }, '');
    }
}

function showDashboardView() {
    document.getElementById('onboardingView').classList.remove('active');
    document.getElementById('dashboardView').classList.add('active');
    document.getElementById('tripManagerHeader').style.display = 'flex';

    // Show copilot sidebar and restore split layout
    const sidebar = document.getElementById('copilotSidebar');
    if (sidebar) sidebar.style.display = 'flex';
    const grid = document.getElementById('workspaceGrid');
    if (grid) grid.classList.remove('onboarding-active');

    // Clear history state if present
    if (history.state && history.state.page === 'onboarding') {
        history.replaceState({ page: 'dashboard' }, '');
    }
}

// Onboarding Chat Functions
let onboardingChatHistory = [];

function appendOnboardingChatMessage(sender, text) {
    const container = document.getElementById('onboardingChatMessages');
    if (!container) return;
    const div = document.createElement('div');
    div.className = `message ${sender}-msg`;
    div.innerHTML = formatMarkdown(text);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

async function handleSendOnboardingMessage(e) {
    e.preventDefault();
    const textarea = document.getElementById('onboardingChatMessageVal');
    const sendBtn = e.target.querySelector('button[type="submit"]');
    const message = textarea.value.trim();
    if (!message) return;

    appendOnboardingChatMessage("user", message);
    onboardingChatHistory.push({ role: "user", text: message });
    textarea.value = '';
    textarea.disabled = true;
    sendBtn.disabled = true;
    const originalPlaceholder = textarea.placeholder;
    textarea.placeholder = "Tola is thinking...";

    let data = null;
    try {
        const res = await fetch('/api/copilot/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                trip_id: null,
                history: onboardingChatHistory
            })
        });

        if (res.ok) {
            data = await res.json();
            appendOnboardingChatMessage("copilot", data.reply);
            onboardingChatHistory.push({ role: "copilot", text: data.reply });

            if (data.created_trip_id) {
                if (data.is_building) {
                    textarea.disabled = true;
                    sendBtn.disabled = true;
                    textarea.placeholder = "Building checklist...";
                    
                    let lastStatus = "";
                    const pollInterval = setInterval(async () => {
                        try {
                            const statusRes = await fetch(`/api/trips/${data.created_trip_id}/build-status`);
                            if (statusRes.ok) {
                                const statusData = await statusRes.json();
                                const status = statusData.status;
                                if (status && status !== lastStatus) {
                                    lastStatus = status;
                                    appendOnboardingChatMessage("system", `⚙️ ${status}`);
                                    
                                    if (status === "Completed") {
                                        clearInterval(pollInterval);
                                        showToast("Workspace checklist compiled!", "success");
                                        setTimeout(async () => {
                                            activeTripId = data.created_trip_id;
                                            document.getElementById('onboardingChatMessages').innerHTML = '';
                                            onboardingChatHistory = [];
                                            await loadTrips();
                                            textarea.disabled = false;
                                            sendBtn.disabled = false;
                                            textarea.placeholder = originalPlaceholder;
                                        }, 1200);
                                    } else if (status.startsWith("Failed:") || status.startsWith("Error:") || status.startsWith("Failed") || status.startsWith("Error")) {
                                        clearInterval(pollInterval);
                                        appendOnboardingChatMessage("system", `❌ Build failed: ${status}`);
                                        textarea.disabled = false;
                                        sendBtn.disabled = false;
                                        textarea.placeholder = originalPlaceholder;
                                    }
                                }
                            }
                        } catch (pollErr) {
                            console.error("Error polling build status:", pollErr);
                        }
                    }, 750);
                } else {
                    showToast("Trip initialized successfully!", "success");
                    setTimeout(async () => {
                        activeTripId = data.created_trip_id;
                        document.getElementById('onboardingChatMessages').innerHTML = '';
                        onboardingChatHistory = [];
                        await loadTrips();
                    }, 1500);
                }
            }
        } else {
            appendOnboardingChatMessage("system", "Error communicating with AI Copilot.");
        }
    } catch (err) {
        appendOnboardingChatMessage("system", "Network error contacting copilot.");
    } finally {
        if (!data || !data.is_building) {
            textarea.disabled = false;
            sendBtn.disabled = false;
            textarea.placeholder = originalPlaceholder;
            textarea.focus();
        }
    }
}

// Archive and Delete Trip functions
async function archiveActiveTrip() {
    const trip = tripsList.find(t => t.trip_id === activeTripId);
    if (!trip) return;

    const currentArchiveState = trip.is_archived === 1;
    const confirmMsg = currentArchiveState 
        ? "Are you sure you want to unarchive this trip checklist?"
        : "Are you sure you want to archive this trip checklist? (Archived lists cannot be edited)";
        
    if (!confirm(confirmMsg)) return;

    try {
        const res = await fetch(`/api/trips/${activeTripId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                trip_name: trip.trip_name,
                start_date: trip.start_date,
                is_archived: !currentArchiveState
            })
        });
        if (res.ok) {
            showToast(currentArchiveState ? "Trip checklist unarchived." : "Trip checklist archived successfully.");
            loadTrips();
        }
    } catch (e) {
        showToast("Error updating trip status.", "error");
    }
}

async function deleteActiveTrip() {
    if (!confirm("WARNING: Are you sure you want to permanently delete this trip and all its checklist items? This action is irreversible.")) return;

    try {
        const res = await fetch(`/api/trips/${activeTripId}`, {
            method: 'DELETE'
        });
        if (res.ok) {
            showToast("Trip checklist deleted.");
            activeTripId = null;
            loadTrips();
        }
    } catch (e) {
        showToast("Error deleting trip.", "error");
    }
}

// Lock UI management
function updateLockUI() {
    const lockIcon = document.getElementById('lockIcon');
    const lockText = document.getElementById('lockText');
    const addItemPanel = document.getElementById('addItemPanel');
    const trip = tripsList.find(t => t.trip_id === activeTripId);

    if (listLocked) {
        lockIcon.className = 'fa-solid fa-lock';
        lockText.innerText = 'Locked';
        lockText.style.color = 'var(--danger)';
        addItemPanel.style.display = 'none';
    } else {
        lockIcon.className = 'fa-solid fa-lock-open';
        lockText.innerText = 'Unlocked';
        lockText.style.color = 'var(--success)';
        if (trip && trip.is_archived === 0) {
            addItemPanel.style.display = 'block';
        }
    }
}

async function toggleEditLock() {
    try {
        const res = await fetch(`/api/trips/${activeTripId}/lock`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ locked: !listLocked })
        });
        if (res.ok) {
            const data = await res.json();
            listLocked = data.locked;
            updateLockUI();
            renderPackingList();
            showToast(listLocked ? "Packing list locked." : "Packing list unlocked.");
        }
    } catch (e) {
        showToast("Error updating lock status.", "error");
    }
}

// CRUD Packing List Items
let draggedElement = null;

function setupDragAndDrop(li) {
    const handle = li.querySelector('.drag-handle');
    if (handle) {
        handle.addEventListener('mousedown', () => {
            li.setAttribute('draggable', 'true');
        });
        handle.addEventListener('mouseup', () => {
            li.setAttribute('draggable', 'false');
        });
    }

    li.addEventListener('dragstart', (e) => {
        if (listLocked) {
            e.preventDefault();
            return;
        }
        draggedElement = li;
        li.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
    });

    li.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        
        const currentGroup = li.closest('.category-group');
        const draggedGroup = draggedElement ? draggedElement.closest('.category-group') : null;
        if (!draggedGroup || currentGroup !== draggedGroup) return;

        const ul = li.parentNode;
        const siblings = Array.from(ul.querySelectorAll('.checklist-item-row:not(.dragging)'));
        
        const nextSibling = siblings.find(sibling => {
            const box = sibling.getBoundingClientRect();
            return e.clientY <= box.top + box.height / 2;
        });

        ul.insertBefore(draggedElement, nextSibling);
    });

    li.addEventListener('dragend', async () => {
        li.classList.remove('dragging');
        li.setAttribute('draggable', 'false');
        draggedElement = null;

        const ul = li.parentNode;
        const rows = Array.from(ul.querySelectorAll('.checklist-item-row'));
        const itemIds = rows.map(row => {
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) {
                const onchangeAttr = checkbox.getAttribute('onchange');
                const match = onchangeAttr.match(/\d+/);
                return match ? parseInt(match[0]) : null;
            }
            return null;
        }).filter(id => id !== null);

        try {
            const res = await fetch(`/api/trips/${activeTripId}/packing/reorder`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item_ids: itemIds })
            });
            if (!res.ok) {
                showToast("Failed to save new order.", "error");
                renderPackingList();
            }
        } catch (err) {
            showToast("Error saving item order.", "error");
            renderPackingList();
        }
    });
}

// CRUD Packing List Items
const collapsedParents = new Set();

function toggleCollapse(parentId) {
    if (collapsedParents.has(parentId)) {
        collapsedParents.delete(parentId);
    } else {
        collapsedParents.add(parentId);
    }
    renderPackingList();
}

async function indentItem(itemId) {
    const rows = Array.from(document.querySelectorAll('.checklist-item-row'));
    const idx = rows.findIndex(r => r.querySelector(`input[onchange*="${itemId}"]`) !== null);
    if (idx === -1) return;
    
    const itemRow = rows[idx];
    if (itemRow.classList.contains('sub-item')) return;

    const catGroup = itemRow.closest('.category-group');
    const groupRootRows = Array.from(catGroup.querySelectorAll('.checklist-item-row:not(.sub-item)'));
    const selfRootIdx = groupRootRows.indexOf(itemRow);
    if (selfRootIdx <= 0) {
        showToast("No preceding item to nest under in this category.", "warning");
        return;
    }
    
    const prevParentRow = groupRootRows[selfRootIdx - 1];
    let prevParentId = null;
    const match = prevParentRow.querySelector('input[type="checkbox"]').getAttribute('onchange').match(/\d+/);
    if (match) {
        prevParentId = parseInt(match[0]);
    }
    
    if (!prevParentId) return;
    
    try {
        const res = await fetch(`/api/trips/${activeTripId}/packing/items/${itemId}/nest`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ parent_id: prevParentId })
        });
        if (res.ok) {
            renderPackingList();
        }
    } catch (err) {
        showToast("Error nesting item.", "error");
    }
}

async function outdentItem(itemId) {
    try {
        const res = await fetch(`/api/trips/${activeTripId}/packing/items/${itemId}/nest`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ parent_id: null })
        });
        if (res.ok) {
            renderPackingList();
        }
    } catch (err) {
        showToast("Error outdenting item.", "error");
    }
}

async function renderPackingList() {
    const container = document.getElementById('packingListItemsContainer');
    container.innerHTML = '';

    try {
        const res = await fetch(`/api/trips/${activeTripId}/packing`);
        if (!res.ok) return;

        const items = await res.json();
        if (items.length === 0) {
            container.innerHTML = `<p class="empty-list-msg">No items in your packing checklist yet.</p>`;
            return;
        }

        // Group by category
        const grouped = {};
        items.forEach(item => {
            const cat = item.category || 'General';
            if (!grouped[cat]) grouped[cat] = [];
            grouped[cat].push(item);
        });

        const trip = tripsList.find(t => t.trip_id === activeTripId);
        const tripArchived = trip && trip.is_archived === 1;

        for (const [cat, catItems] of Object.entries(grouped)) {
            const catDiv = document.createElement('div');
            catDiv.className = 'category-group';
            catDiv.innerHTML = `<h3>${cat}</h3>`;

            const listUl = document.createElement('ul');
            listUl.className = 'checklist-ul';

            // Reconstruct hierarchy in this category
            const itemMap = {};
            catItems.forEach(item => { itemMap[item.id] = item; });
            
            const roots = [];
            const childrenMap = {};
            catItems.forEach(item => {
                const parentId = item.parent_id;
                if (parentId && itemMap[parentId]) {
                    if (!childrenMap[parentId]) childrenMap[parentId] = [];
                    childrenMap[parentId].push(item);
                } else {
                    roots.push(item);
                }
            });

            const renderItem = (item, isSubItem, hasChildren) => {
                const li = document.createElement('li');
                const highPriorityClass = item.priority === 'High' ? 'priority-high' : '';
                const subClass = isSubItem ? 'sub-item' : '';
                li.className = `checklist-item-row ${highPriorityClass} ${subClass}`;
                
                const isChecked = item.is_checked ? 'checked' : '';
                const disabled = (tripArchived || listLocked) ? 'disabled' : '';
                
                let dragHandleHTML = '';
                if (!tripArchived && !listLocked) {
                    dragHandleHTML = `<span class="drag-handle" title="Drag to reorder"><i class="fa-solid fa-grip-vertical"></i></span>`;
                }

                let caretHTML = '';
                if (!isSubItem && hasChildren) {
                    const isCollapsed = collapsedParents.has(item.id);
                    caretHTML = `
                        <button class="btn-icon caret-btn" onclick="toggleCollapse(${item.id})">
                            <i class="fa-solid ${isCollapsed ? 'fa-caret-right' : 'fa-caret-down'}"></i>
                        </button>
                    `;
                } else if (!isSubItem) {
                    caretHTML = `<span class="caret-placeholder"></span>`;
                }
                
                let indentButtonHTML = '';
                if (!tripArchived && !listLocked) {
                    if (isSubItem) {
                        indentButtonHTML = `
                            <button class="btn-icon" onclick="outdentItem(${item.id})" title="Outdent">
                                <i class="fa-solid fa-outdent"></i>
                            </button>
                        `;
                    } else {
                        indentButtonHTML = `
                            <button class="btn-icon" onclick="indentItem(${item.id})" title="Indent">
                                <i class="fa-solid fa-indent"></i>
                            </button>
                        `;
                    }
                }
                
                const searchQ = item.is_private 
                    ? encodeURIComponent((item.category || 'General') + ' travel packing')
                    : encodeURIComponent(item.item_name + ' travel');
                const searchUrl = `https://www.google.com/search?q=${searchQ}`;

                li.innerHTML = `
                    ${dragHandleHTML}
                    ${caretHTML}
                    <input type="checkbox" ${isChecked} ${disabled} onchange="toggleCheck(${item.id}, this.checked)">
                    <div class="item-content-cols">
                        <div class="item-label-row">
                            <a href="${searchUrl}" target="_blank" class="item-name-link" title="Search Google for ${item.item_name}">${item.item_name}</a>
                            <input type="number" class="item-qty-input" value="${item.quantity}" min="0" max="99" ${disabled} 
                                   onchange="updateQuantity(${item.id}, this.value, ${item.quantity})" 
                                   onkeypress="if(event.key==='Enter') this.blur()">
                        </div>
                        <input type="text" class="item-desc-input" value="${item.description || ''}" ${disabled} 
                               placeholder="Add description/notes..." onblur="updateDescription(${item.id}, this.value)" 
                               onkeypress="if(event.key==='Enter') this.blur()">
                    </div>
                    <div class="item-actions">
                        ${indentButtonHTML}
                        <button class="btn-icon" ${disabled} onclick="deleteItem(${item.id})" title="Delete"><i class="fa-solid fa-trash"></i></button>
                    </div>
                `;
                
                if (!tripArchived && !listLocked) {
                    setupDragAndDrop(li);
                }
                
                listUl.appendChild(li);
            };

            roots.forEach(item => {
                const hasChildren = childrenMap[item.id] && childrenMap[item.id].length > 0;
                renderItem(item, false, hasChildren);
                
                if (hasChildren && !collapsedParents.has(item.id)) {
                    childrenMap[item.id].forEach(child => {
                        renderItem(child, true, false);
                    });
                }
            });

            catDiv.appendChild(listUl);
            container.appendChild(catDiv);
        }
    } catch (err) {
        console.error("Error rendering packing list:", err);
    }
}

async function toggleCheck(id, checked) {
    try {
        const res = await fetch(`/api/trips/${activeTripId}/packing/items/${id}/check`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_checked: checked })
        });
        if (!res.ok) {
            showToast("Failed to toggle check status.", "error");
            renderPackingList();
        }
    } catch (e) {
        showToast("Error updating checkbox.", "error");
    }
}

async function updateQuantity(id, newVal, oldVal) {
    const num = Number(newVal);
    if (!Number.isInteger(num) || num < 0 || num > 99) {
        showToast("Quantity must be a whole number between 0 and 99.", "error");
        renderPackingList();
        return;
    }
    if (num === 0) {
        if (confirm("Are you sure you want to delete this item?")) {
            await deleteItem(id);
        } else {
            renderPackingList();
        }
        return;
    }
    try {
        const listRes = await fetch(`/api/trips/${activeTripId}/packing`);
        const items = await listRes.json();
        const item = items.find(i => i.id === id);
        if (!item) return;

        const res = await fetch(`/api/trips/${activeTripId}/packing/items/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                item_name: item.item_name,
                quantity: num,
                category: item.category,
                priority: item.priority,
                is_private: item.is_private ? true : false,
                description: item.description || ""
            })
        });

        if (res.ok) {
            showToast("Quantity updated.");
            renderPackingList();
        } else {
            const data = await res.json();
            showToast(data.detail || "Validation failed for quantity.", "error");
            renderPackingList();
        }
    } catch (e) {
        showToast("Error updating quantity.", "error");
        renderPackingList();
    }
}

async function updateDescription(id, desc) {
    try {
        const listRes = await fetch(`/api/trips/${activeTripId}/packing`);
        const items = await listRes.json();
        const item = items.find(i => i.id === id);
        if (!item) return;

        const res = await fetch(`/api/trips/${activeTripId}/packing/items/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                item_name: item.item_name,
                quantity: item.quantity,
                category: item.category,
                priority: item.priority,
                is_private: item.is_private ? true : false,
                description: desc
            })
        });

        if (res.ok) {
            showToast("Notes updated.");
        } else {
            const data = await res.json();
            showToast(data.detail || "Validation failed for notes.", "error");
            renderPackingList();
        }
    } catch (e) {
        showToast("Error saving description.", "error");
    }
}

async function deleteItem(id) {
    try {
        const res = await fetch(`/api/trips/${activeTripId}/packing/items/${id}`, {
            method: 'DELETE'
        });
        if (res.ok) {
            showToast("Item deleted.");
            renderPackingList();
        } else {
            showToast("Failed to delete item.", "error");
        }
    } catch (e) {
        showToast("Error deleting item.", "error");
    }
}

async function handleAddPackingItem(e) {
    e.preventDefault();
    const item_name = document.getElementById('addName').value;
    const quantity = parseInt(document.getElementById('addQty').value) || 1;
    const category = document.getElementById('addCategory').value || "General";
    const priority = document.getElementById('addPriority').value;
    const isPrivate = false;
    const description = document.getElementById('addDesc').value;

    const errBox = document.getElementById('addItemError');
    errBox.innerText = '';

    try {
        const res = await fetch(`/api/trips/${activeTripId}/packing/items`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                item_name, quantity, category, priority, is_private: isPrivate, description
            })
        });

        if (res.ok) {
            showToast("Item added successfully.");
            document.getElementById('addName').value = '';
            document.getElementById('addDesc').value = '';
            document.getElementById('addQty').value = '1';
            renderPackingList();
        } else {
            const data = await res.json();
            errBox.innerText = data.detail || "Validation check failed.";
        }
    } catch (err) {
        showToast("Network error creating item.", "error");
    }
}

// PDF Downloader
function triggerPdfExport() {
    const pf = document.getElementById('pdfPrinterFriendly').checked;
    const tripId = String(activeTripId || '').trim();
    if (!/^[A-Za-z0-9_-]+$/.test(tripId)) {
        showToast("Invalid trip selected.", "error");
        return;
    }
    let url = `/api/trips/${encodeURIComponent(tripId)}/export/pdf`;
    if (pf) {
        url += `?printer_friendly=true`;
    }
    window.location.href = url;
}

// Markdown Downloader & Copy to Clipboard
async function triggerMarkdownExport() {
    if (!activeTripId) return;
    try {
        const res = await fetch(`/api/trips/${activeTripId}/export/markdown`);
        if (res.ok) {
            const mdText = await res.text();
            const blob = new Blob([mdText], { type: 'text/markdown' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `packing_list_${activeTripId}.md`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            showToast("Markdown checklist downloaded successfully!", "success");
        } else {
            showToast("Error exporting Markdown.", "error");
        }
    } catch (err) {
        showToast("Network error exporting Markdown.", "error");
    }
}

async function copyMarkdownToClipboard() {
    if (!activeTripId) return;
    try {
        const res = await fetch(`/api/trips/${activeTripId}/export/markdown`);
        if (res.ok) {
            const mdText = await res.text();
            await navigator.clipboard.writeText(mdText);
            showToast("Markdown copied to clipboard!", "success");
        } else {
            showToast("Error exporting Markdown.", "error");
        }
    } catch (err) {
        showToast("Network error copying Markdown.", "error");
    }
}

// Copilot Chat Sidebar
function appendCopilotMessage(sender, text) {
    const container = document.getElementById('copilotChatMessages');
    const div = document.createElement('div');
    div.className = `message ${sender}-msg`;
    div.innerHTML = formatMarkdown(text);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

async function handleSendCopilotMessage(e) {
    e.preventDefault();
    const textarea = document.getElementById('copilotChatMessageVal');
    const message = textarea.value.trim();
    if (!message) return;

    appendCopilotMessage("user", message);
    textarea.value = '';

    try {
        const res = await fetch('/api/copilot/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message, trip_id: activeTripId })
        });

        if (res.ok) {
            const data = await res.json();
            appendCopilotMessage("copilot", data.reply);
            
            // Always refresh packing list display to capture any added/modified/deleted items
            await renderPackingList();

            if (data.regenerated) {
                await loadTrips();
                await selectActiveTripUI();
                showToast("Trip checklist regenerated successfully.");
            }
        } else {
            appendCopilotMessage("system", "Error communicating with AI Copilot.");
        }
    } catch (err) {
        appendCopilotMessage("system", "Network error contacting copilot.");
    }
}

// Toast Notifications
function showToast(message, type = "success") {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerText = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

// ============================================================
// Packing Item Hover Tooltip
// ============================================================

// Category-level fallback images (used for private items)
const CATEGORY_IMAGES = {
    'Medical':       'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&q=80',
    'Medications':   'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&q=80',
    'Clothing':      'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&q=80',
    'Electronics':   'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=300&q=80',
    'Toiletries':    'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=300&q=80',
    'Hygiene':       'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=300&q=80',
    'Entertainment': 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=300&q=80',
    'Documents':     'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=300&q=80',
    'Accessories':   'https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=300&q=80',
    'Tasks':         'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=300&q=80',
    'Food':          'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=300&q=80',
    'General':       'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=300&q=80',
};

// Keyword-to-image map for public items (matched against item name)
const ITEM_KEYWORD_IMAGES = [
    { keywords: ['passport', 'id', 'document', 'visa'],           url: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=300&q=80' },
    { keywords: ['shirt', 't-shirt', 'tshirt', 'top', 'jersey'],  url: 'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=300&q=80' },
    { keywords: ['pants', 'trousers', 'jeans', 'shorts'],         url: 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=300&q=80' },
    { keywords: ['underwear', 'bra', 'boxers', 'briefs'],         url: 'https://images.unsplash.com/photo-1616150638538-ffb0679a3fc4?w=300&q=80' },
    { keywords: ['jacket', 'coat', 'raincoat', 'windbreaker'],    url: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=300&q=80' },
    { keywords: ['shoes', 'boots', 'sneakers', 'sandals', 'booties'], url: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&q=80' },
    { keywords: ['socks'],                                        url: 'https://images.unsplash.com/photo-1586350977771-b3714d56a8d4?w=300&q=80' },
    { keywords: ['hat', 'cap', 'beanie'],                         url: 'https://images.unsplash.com/photo-1521369909029-2afed882baee?w=300&q=80' },
    { keywords: ['sunglasses', 'glasses'],                        url: 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=300&q=80' },
    { keywords: ['charger', 'adapter', 'plug', 'cable'],          url: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&q=80' },
    { keywords: ['phone', 'mobile', 'smartphone'],                url: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&q=80' },
    { keywords: ['laptop', 'computer', 'macbook'],                url: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&q=80' },
    { keywords: ['camera', 'gopro', 'lens'],                      url: 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300&q=80' },
    { keywords: ['headphones', 'earbuds', 'airpods'],             url: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&q=80' },
    { keywords: ['toothbrush', 'toothpaste', 'dental', 'floss'],  url: 'https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=300&q=80' },
    { keywords: ['shampoo', 'conditioner', 'soap', 'body wash'],  url: 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=300&q=80' },
    { keywords: ['makeup', 'cosmetics', 'lipstick', 'foundation', 'mascara', 'blush', 'polish'], url: 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300&q=80' },
    { keywords: ['deodorant'],                                    url: 'https://images.unsplash.com/photo-1618330834871-dd22c2c226ca?w=300&q=80' },
    { keywords: ['perfume', 'cologne', 'fragrance', 'scent'],     url: 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=300&q=80' },
    { keywords: ['razor', 'shaver', 'shaving'],                   url: 'https://images.unsplash.com/photo-1626245917897-4f617f9cd8d8?w=300&q=80' },
    { keywords: ['rolex', 'watch', 'smartwatch'],                 url: 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=300&q=80' },
    { keywords: ['sunscreen', 'sunblock', 'spf'],                 url: 'https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?w=300&q=80' },
    { keywords: ['umbrella', 'rain'],                             url: 'https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=300&q=80' },
    { keywords: ['book', 'journal', 'notebook'],                  url: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&q=80' },
    { keywords: ['backpack', 'bag', 'luggage', 'suitcase'],       url: 'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=300&q=80' },
    { keywords: ['wallet', 'money', 'cash', 'cards'],             url: 'https://images.unsplash.com/photo-1627843240167-b1f9d28f732b?w=300&q=80' },
    { keywords: ['inhaler', 'epipen', 'first aid', 'bandage', 'pill', 'medicine', 'prescription', 'zoloft', 'benadryl'], url: 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&q=80' },
    { keywords: ['snack', 'food', 'bar', 'energy'],               url: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=300&q=80' },
    { keywords: ['water bottle', 'bottle', 'flask'],              url: 'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=300&q=80' },
    { keywords: ['lock', 'padlock'],                              url: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&q=80' },
    { keywords: ['power bank', 'battery', 'portable charger'],   url: 'https://images.unsplash.com/photo-1613665813446-82a78c468a1d?w=300&q=80' },
    { keywords: ['towel', 'beach towel'],                         url: 'https://images.unsplash.com/photo-1600480896351-8f5e17cb4a54?w=300&q=80' },
    { keywords: ['mask', 'face mask'],                            url: 'https://images.unsplash.com/photo-1584634731339-252c581abfc5?w=300&q=80' },
];

/**
 * Sanitize a cleaned item name into comma-separated search keywords.
 * Strips grammar noise, travel verbs, and adjectives that cause bad image search results.
 */
function sanitizeImageSearchTerms(cleanName) {
    const NOISE_WORDS = new Set([
        // Grammar / structural noise
        'a','an','the','of','for','to','and','or','with','in','on','at','by','from','your','my','its','is','are',
        'x','qty','ea','pc','pcs','set','pair','pairs','pack','size','large','small','medium','extra','xl','xs',
        
        // Travel / list generic words
        'book', 'booking', 'reserve', 'reservation', 'make', 'arrange', 'verify', 'file', 'needed', 'required', 
        'warning', 'alert', 'travel', 'trip', 'checklist', 'permit', 'ticket', 'entry', 'pre-trip',
        
        // Adjectives & modifiers that cause unrelated Unsplash matches
        'comfortable', 'walking', 'running', 'hiking', 'swimming', 'climbing', 'waterproof', 'windproof', 
        'rainproof', 'insulated', 'thermal', 'heavy', 'light', 'lightweight', 'warm', 'cold', 'cool', 'mild', 
        'hot', 'tropical', 'desert', 'alpine', 'freezing', 'sub-zero', 'breathable', 'modest', 'personal', 
        'prescription', 'embassy', 'permit', 'timed', 'timed-entry', 'advanced', 'local', 'casual'
    ]);
    return cleanName
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, ' ')       // strip special chars
        .split(/\s+/)                         // tokenize
        .filter(w => w.length > 1 && !NOISE_WORDS.has(w) && !/^\d+$/.test(w))
        .slice(0, 4)                          // max 4 keywords
        .join(',');
}

/**
 * Returns the best image URL for a given packing item.
 *
 * Resolution order (public items):
 *   1. Curated keyword map  — high-quality Unsplash photos for common travel items
 *   2. Dynamic placeholder  — derives search terms from the cleaned item name via LoremFlickr
 *   3. Category fallback    — generic category-level Unsplash image
 *
 * Private items always get the category-level fallback (no name exposure).
 */
function getItemImageUrl(itemName, category, isPrivate) {
    if (isPrivate) {
        return CATEGORY_IMAGES[category] || CATEGORY_IMAGES['General'];
    }

    // Clean name: strip " for [Traveler]" suffix, parentheses, brackets, and possessives
    let cleanName = itemName;
    cleanName = cleanName.replace(/\([^)]*\)/g, '').trim();
    cleanName = cleanName.replace(/\[[^\]]*\]/g, '').trim();
    cleanName = cleanName.replace(/\b[a-z0-9]+\'s\b/gi, '').trim();
    cleanName = cleanName.replace(/\s+for\s+.+$/i, '').trim();

    // 1. Check curated keyword map
    const nameLower = cleanName.toLowerCase();
    for (const entry of ITEM_KEYWORD_IMAGES) {
        if (entry.keywords.some(kw => nameLower.includes(kw))) {
            return entry.url;
        }
    }

    // 2. Dynamic placeholder fallback (using LoremFlickr tag search as Unsplash Source is deprecated)
    const terms = sanitizeImageSearchTerms(cleanName);
    if (terms) {
        return `https://loremflickr.com/300/300/travel,${encodeURIComponent(terms)}`;
    }

    // 3. Category fallback
    return CATEGORY_IMAGES[category] || CATEGORY_IMAGES['General'];
}

const _getTooltip     = () => document.getElementById('itemTooltipPopover');
const _getTooltipImg  = () => document.getElementById('tooltipImage');
const _getTooltipLink = () => document.getElementById('tooltipSearchLink');

let _tooltipHideTimer = null;

function onItemRowMouseEnter(e) {
    clearTimeout(_tooltipHideTimer);
    const li        = e.currentTarget;
    const itemName  = li.dataset.itemName;
    const category  = li.dataset.category;
    const isPrivate = li.dataset.isPrivate === 'true';

    const imgUrl  = getItemImageUrl(itemName, category, isPrivate);
    // Private items: search by generic category phrase to avoid leaking item name
    const searchQ = isPrivate
        ? encodeURIComponent(category + ' travel packing')
        : encodeURIComponent(itemName + ' travel');

    _getTooltipImg().src   = imgUrl;
    _getTooltipImg().alt   = isPrivate ? category : itemName;
    _getTooltipLink().href = `https://www.google.com/search?q=${searchQ}`;

    const tip = _getTooltip();
    tip.style.display = 'block';
    _positionTooltip(e);
}

function onItemRowMouseMove(e) {
    _positionTooltip(e);
}

function onItemRowMouseLeave() {
    _tooltipHideTimer = setTimeout(() => {
        const tip = _getTooltip();
        if (tip) tip.style.display = 'none';
    }, 120);
}

function _positionTooltip(e) {
    const tip     = _getTooltip();
    const margin  = 16;
    const tipW    = tip.offsetWidth  || 240;
    const tipH    = tip.offsetHeight || 250;
    const vpW     = window.innerWidth;
    const vpH     = window.innerHeight;
    const scrollX = window.scrollX;
    const scrollY = window.scrollY;

    let x = e.clientX + margin + scrollX;
    let y = e.clientY + margin + scrollY;

    // Flip horizontally if overflow right edge
    if (e.clientX + margin + tipW > vpW) {
        x = e.clientX - margin - tipW + scrollX;
    }
    // Flip vertically if overflow bottom edge
    if (e.clientY + margin + tipH > vpH) {
        y = e.clientY - margin - tipH + scrollY;
    }

    tip.style.left = x + 'px';
    tip.style.top  = y + 'px';
}

// Keep tooltip alive if cursor moves into the popover itself
document.addEventListener('DOMContentLoaded', () => {
    const tip = _getTooltip();
    if (tip) {
        tip.addEventListener('mouseenter', () => clearTimeout(_tooltipHideTimer));
        tip.addEventListener('mouseleave', onItemRowMouseLeave);
    }
});

// Window navigation safeguards
window.addEventListener('beforeunload', (event) => {
    const onboardingActive = document.getElementById('onboardingView')?.classList.contains('active');
    if (onboardingActive && onboardingChatHistory.length > 1) {
        event.preventDefault();
        event.returnValue = 'Your trip onboarding details are not saved yet. Are you sure you want to leave?';
        return event.returnValue;
    }
});

window.addEventListener('popstate', (event) => {
    const onboardingActive = document.getElementById('onboardingView')?.classList.contains('active');
    if (onboardingActive && onboardingChatHistory.length > 1) {
        if (!confirm("Your trip onboarding details are not saved yet. Are you sure you want to leave?")) {
            // Push the state back to stay on onboarding
            history.pushState({ page: 'onboarding' }, '');
            return;
        }
    }
    if (tripsList.length > 0) {
        showDashboardView();
    }
});
