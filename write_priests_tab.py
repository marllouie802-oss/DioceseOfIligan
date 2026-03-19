
import os

content = r"""{% load static %}
{# Priests Tab Content - Manage parish priests/ministers #}
<div class="tab-panel" id="priests">
  <div class="tab-header">
    <h2>Priests & Ministers</h2>
    <p>Manage priests and ministers available for services in your parish</p>
  </div>
  <div class="tab-content">

    {# Info Card #}
    <div class="admin-info-section">
      <div class="info-card" style="background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);">
        <div class="info-card-header">
          <div class="info-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4M12 8h.01"/>
            </svg>
          </div>
          <div>
            <h3>Parish Priests & Ministers</h3>
            <p>Add priests and ministers who can be assigned to service appointments. Parishioners can select from available priests when scheduling interviews.</p>
          </div>
        </div>
      </div>
    </div>

    {# Priests List Section #}
    <div class="admin-section">
      <div class="section-header-with-action">
        <div class="section-header-left">
          <div class="role-badge" style="background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); color: white;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <span>Parish Priests</span>
          </div>
          <p class="role-description">Priests and ministers available for appointment services</p>
        </div>
        <button class="btn-add-member" onclick="openAddPriestModal()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Add Priest
        </button>
      </div>

      <div class="admin-table-wrapper">
        <table class="admin-table" id="priestsTable">
          <thead>
            <tr>
              <th>Name & Title</th>
              <th>Contact</th>
              <th>Specializations</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {% if priests %}
              {% for priest in priests %}
              <tr data-priest-id="{{ priest.id }}">
                <td>
                  <div class="admin-user-cell">
                    <div class="admin-avatar">
                      {% if priest.photo %}
                        <img src="{{ priest.photo.url }}" alt="{{ priest.full_title }}">
                      {% else %}
                        <div class="avatar-placeholder" style="background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);">
                          {{ priest.name|slice:":1"|upper }}
                        </div>
                      {% endif %}
                    </div>
                    <div class="admin-user-info">
                      <span class="admin-name">{{ priest.full_title }}</span>
                      <span class="admin-role-label">{{ priest.title }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <div style="font-size: 0.875rem;">
                    {% if priest.email %}<div>{{ priest.email }}</div>{% endif %}
                    {% if priest.phone %}<div style="color: var(--muted);">{{ priest.phone }}</div>{% endif %}
                    {% if not priest.email and not priest.phone %}<span style="color: var(--muted);">Not provided</span>{% endif %}
                  </div>
                </td>
                <td>
                  <div style="font-size: 0.875rem; max-width: 200px;">
                    {% if priest.specializations %}
                      {{ priest.specializations|truncatewords:10 }}
                    {% else %}
                      <span style="color: var(--muted);">None specified</span>
                    {% endif %}
                  </div>
                </td>
                <td>
                  <span class="status-badge {% if priest.is_available %}status-active{% else %}status-inactive{% endif %}">
                    {% if priest.is_available %}Available{% else %}Unavailable{% endif %}
                  </span>
                </td>
                <td>
                  <div style="display: flex; gap: 0.5rem;">
                    <button class="btn-table-action" onclick="openEditPriestModal('{{ priest.id }}')">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                      </svg>
                      Edit
                    </button>
                    <button class="btn-table-action" style="color: #dc2626; border-color: #dc2626;" onclick="confirmDeletePriest('{{ priest.id }}', '{{ priest.full_title|escapejs }}')">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                      </svg>
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
              {% endfor %}
            {% else %}
            <tr>
              <td colspan="5" class="empty-cell">
                <div class="empty-state-small">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  <p>No priests added yet</p>
                  <small>Click "Add Priest" to add ministers who can be assigned to appointments</small>
                </div>
              </td>
            </tr>
            {% endif %}
          </tbody>
        </table>
      </div>
    </div>

  </div>
</div>

{# Add/Edit Priest Modal #}
<div id="priestModal" class="staff-modal" style="display: none;">
  <div class="staff-modal-overlay" onclick="closePriestModal()"></div>
  <div class="staff-modal-content" style="max-width: 600px;">
    <div class="staff-modal-header">
      <h3 id="priestModalTitle">Add Priest</h3>
      <button type="button" class="staff-modal-close" onclick="closePriestModal()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>
    
    <div class="staff-modal-body">
      <form id="priestForm" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="hidden" id="priestId" name="priest_id" value="">
        
        <div class="form-row">
          <div class="form-group" style="flex: 1;">
            <label for="priestTitle">Title *</label>
            <select id="priestTitle" name="title" class="form-control" required>
              <option value="Rev. Fr.">Rev. Fr. (Reverend Father)</option>
              <option value="Fr.">Fr. (Father)</option>
              <option value="Msgr.">Msgr. (Monsignor)</option>
              <option value="Most Rev.">Most Rev. (Bishop)</option>
              <option value="Deacon">Deacon</option>
              <option value="Bro.">Bro. (Brother)</option>
              <option value="Sr.">Sr. (Sister)</option>
              <option value="Minister">Minister</option>
              <option value="Pastor">Pastor</option>
            </select>
          </div>
          <div class="form-group" style="flex: 2;">
            <label for="priestName">Full Name *</label>
            <input type="text" id="priestName" name="name" class="form-control" required placeholder="e.g., Juan dela Cruz">
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group" style="flex: 1;">
            <label for="priestEmail">Email</label>
            <input type="email" id="priestEmail" name="email" class="form-control" placeholder="email@parish.org">
          </div>
          <div class="form-group" style="flex: 1;">
            <label for="priestPhone">Phone</label>
            <input type="tel" id="priestPhone" name="phone" class="form-control" placeholder="+63 912 345 6789">
          </div>
        </div>
        
        <div class="form-group">
          <label for="priestSpecializations">Specializations</label>
          <textarea id="priestSpecializations" name="specializations" class="form-control" rows="2" placeholder="e.g., Baptism, Wedding, Counseling, Mass, Confession"></textarea>
          <small class="form-text">Services or sacraments this priest can officiate</small>
        </div>
        
        <div class="form-group">
          <label for="priestBio">Biography</label>
          <textarea id="priestBio" name="bio" class="form-control" rows="3" placeholder="Brief background or description..."></textarea>
        </div>
        
        <div class="form-group">
          <label for="priestPhoto">Photo</label>
          <input type="file" id="priestPhoto" name="photo" class="form-control" accept="image/*">
          <div id="priestPhotoPreview" style="margin-top: 10px; display: none;">
            <img src="" alt="Preview" style="max-width: 100px; max-height: 100px; border-radius: 8px; object-fit: cover;">
          </div>
        </div>
        
        <div class="form-group">
          <label class="checkbox-label">
            <input type="checkbox" id="priestAvailable" name="is_available" checked>
            <span>Available for appointments</span>
          </label>
        </div>
        
        <div class="staff-modal-actions" style="margin-top: 1.5rem;">
          <button type="button" class="btn btn-outline" onclick="closePriestModal()">Cancel</button>
          <button type="submit" class="btn btn-primary" id="priestSubmitBtn">
            <span id="priestSubmitText">Add Priest</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

{# Delete Confirmation Modal #}
<div id="deletePriestModal" class="staff-modal" style="display: none;">
  <div class="staff-modal-overlay" onclick="closeDeletePriestModal()"></div>
  <div class="staff-modal-content" style="max-width: 450px;">
    <div class="staff-modal-header">
      <h3>Delete Priest</h3>
      <button type="button" class="staff-modal-close" onclick="closeDeletePriestModal()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>
    
    <div class="staff-modal-body">
      <div style="display: flex; align-items: flex-start; gap: 15px; padding: 20px; background: #fef2f2; border-left: 4px solid #dc2626; border-radius: 4px; margin-bottom: 20px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" style="width: 24px; height: 24px; flex-shrink: 0;">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        <div>
          <p style="margin: 0 0 10px 0; font-weight: 600; color: #991b1b;">Are you sure you want to delete this priest?</p>
          <p style="margin: 0; color: #991b1b; font-size: 14px;">This action cannot be undone. Any bookings assigned to this priest will need to be reassigned.</p>
        </div>
      </div>
      
      <p style="margin-bottom: 20px;"><strong>Priest:</strong> <span id="deletePriestName"></span></p>
      
      <div class="staff-modal-actions">
        <button type="button" class="btn btn-outline" onclick="closeDeletePriestModal()">Cancel</button>
        <button type="button" class="btn btn-danger" onclick="deletePriest()" id="confirmDeletePriestBtn">Delete Priest</button>
      </div>
    </div>
  </div>
</div>

<script>
// Priest Management JavaScript
let currentPriestId = null;
let deletePriestId = null;

function openAddPriestModal() {
    currentPriestId = null;
    document.getElementById('priestModalTitle').textContent = 'Add Priest';
    document.getElementById('priestSubmitText').textContent = 'Add Priest';
    document.getElementById('priestForm').reset();
    document.getElementById('priestId').value = '';
    document.getElementById('priestPhotoPreview').style.display = 'none';
    document.getElementById('priestModal').style.display = 'flex';
}

function openEditPriestModal(priestId) {
    currentPriestId = priestId;
    document.getElementById('priestModalTitle').textContent = 'Edit Priest';
    document.getElementById('priestSubmitText').textContent = 'Save Changes';
    document.getElementById('priestId').value = priestId;
    
    // Fetch priest data
    fetch(`/app/api/church/${CURRENT_CHURCH_ID}/priests/${priestId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const priest = data.priest;
                document.getElementById('priestTitle').value = priest.title || 'Rev. Fr.';
                document.getElementById('priestName').value = priest.name || '';
                document.getElementById('priestEmail').value = priest.email || '';
                document.getElementById('priestPhone').value = priest.phone || '';
                document.getElementById('priestSpecializations').value = priest.specializations || '';
                document.getElementById('priestBio').value = priest.bio || '';
                document.getElementById('priestAvailable').checked = priest.is_available;
                
                // Show photo preview if exists
                if (priest.photo_url) {
                    const preview = document.getElementById('priestPhotoPreview');
                    preview.querySelector('img').src = priest.photo_url;
                    preview.style.display = 'block';
                } else {
                    document.getElementById('priestPhotoPreview').style.display = 'none';
                }
                
                document.getElementById('priestModal').style.display = 'flex';
            } else {
                alert('Error loading priest data: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load priest data');
        });
}

function closePriestModal() {
    document.getElementById('priestModal').style.display = 'none';
    currentPriestId = null;
}

function confirmDeletePriest(priestId, priestName) {
    deletePriestId = priestId;
    document.getElementById('deletePriestName').textContent = priestName;
    document.getElementById('deletePriestModal').style.display = 'flex';
}

function closeDeletePriestModal() {
    document.getElementById('deletePriestModal').style.display = 'none';
    deletePriestId = null;
}

function deletePriest() {
    if (!deletePriestId) return;
    
    const btn = document.getElementById('confirmDeletePriestBtn');
    btn.disabled = true;
    btn.textContent = 'Deleting...';
    
    fetch(`/app/api/church/${CURRENT_CHURCH_ID}/priests/${deletePriestId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove row from table
            const row = document.querySelector(`tr[data-priest-id="${deletePriestId}"]`);
            if (row) row.remove();
            
            // Check if table is empty
            const tbody = document.querySelector('#priestsTable tbody');
            if (tbody && tbody.querySelectorAll('tr[data-priest-id]').length === 0) {
                tbody.innerHTML = `
                    <tr>
                      <td colspan="5" class="empty-cell">
                        <div class="empty-state-small">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                          </svg>
                          <p>No priests added yet</p>
                          <small>Click "Add Priest" to add ministers who can be assigned to appointments</small>
                        </div>
                      </td>
                    </tr>
                `;
            }
            
            closeDeletePriestModal();
        } else {
            alert('Error deleting priest: ' + (data.message || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to delete priest');
    })
    .finally(() => {
        btn.disabled = false;
        btn.textContent = 'Delete Priest';
    });
}

// Photo preview
document.getElementById('priestPhoto')?.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('priestPhotoPreview');
            preview.querySelector('img').src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

// Form submission
document.getElementById('priestForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const form = this;
    const formData = new FormData(form);
    const priestId = document.getElementById('priestId').value;
    const isEdit = priestId && priestId !== '';
    
    const btn = document.getElementById('priestSubmitBtn');
    const btnText = document.getElementById('priestSubmitText');
    const originalText = btnText.textContent;
    
    btn.disabled = true;
    btnText.textContent = isEdit ? 'Saving...' : 'Adding...';
    
    const url = isEdit 
        ? `/app/api/church/${CURRENT_CHURCH_ID}/priests/${priestId}/update/`
        : `/app/api/church/${CURRENT_CHURCH_ID}/priests/create/`;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload the page to show updated list
            window.location.reload();
        } else {
            alert('Error: ' + (data.message || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to save priest');
    })
    .finally(() => {
        btn.disabled = false;
        btnText.textContent = originalText;
    });
});
</script>

<style>
/* Additional styles for Priests tab */
.form-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.form-row .form-group {
    margin-bottom: 0;
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.checkbox-label input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: var(--brand);
}

.btn-danger {
    background: #dc2626;
    color: white;
    border: none;
}

.btn-danger:hover {
    background: #b91c1c;
}

@media (max-width: 768px) {
    .form-row {
        flex-direction: column;
    }
}
</style>
"""

with open('templates/partials/manage/priests_tab.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('File written successfully')
