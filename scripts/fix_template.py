import os

for file in ['create_service.html', 'edit_service.html']:
    path = f'c:/Users/asus/CascadeProjects/ChurchIligan/templates/core/{file}'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if UI replacement is already there
    if 'id="service-time-slot-list"' not in content:
        # Search more fuzzily for the target text
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'for="{{ form.available_time_slots.id_for_label }}"' in line or 'available_time_slots' in line and '<label' in line:
                start_idx = i
                end_idx = i
                for j in range(i, i+15): # expanded search space slightly
                    if '<small class="form-help">Comma-separated' in lines[j] or 'of open scheduling (e.g.,' in lines[j]:
                         end_idx = j
                         if 'of open' in lines[j] or '</small>' in lines[j]:
                            if 'of open scheduling (' in lines[j] and '</small>' not in lines[j]:
                                end_idx = j + 1
                                break
                            break
                            
                    # Alternate case: error divs might be present instead of small text immediately
                    if 'form.available_time_slots.errors' in lines[j]:
                         end_idx = j-1 # replace up to but not including the error block
                         break
                
                # We found the block
                replacement = '''              <label class="form-label" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Available Time Slots</label>
              <input type="hidden" id="id_available_time_slots" name="available_time_slots" value="{{ form.available_time_slots.value|default_if_none:'' }}">
              
              <div id="service-time-slot-list" style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; margin-top: 8px;">
                <!-- Dynamic tags will go here -->
              </div>
              
              <div style="display: flex; align-items: center; gap: 10px; background: #f8fafc; padding: 12px; border: 1px solid #e2e8f0; border-radius: 6px;">
                <div style="display: flex; flex-direction: column; flex: 1;">
                  <label for="serviceNewSlotStart" style="font-size: 0.75rem; margin-bottom: 2px;">Start Time</label>
                  <input type="time" id="serviceNewSlotStart" class="form-control" style="padding: 6px;">
                </div>
                <span style="color: #64748b;">to</span>
                <div style="display: flex; flex-direction: column; flex: 1;">
                  <label for="serviceNewSlotEnd" style="font-size: 0.75rem; margin-bottom: 2px;">End Time</label>
                  <input type="time" id="serviceNewSlotEnd" class="form-control" style="padding: 6px;">
                </div>
                <button type="button" class="btn btn-primary" onclick="addServiceTimeSlot()" style="margin-top: 16px; padding: 6px 16px; white-space: nowrap;">
                  + Add
                </button>
              </div>
              <small class="form-help">Add specific time ranges if you want people to pick from specific times instead of open scheduling</small>'''
                lines[start_idx:end_idx+1] = [replacement]
                content = '\n'.join(lines)
                break
                
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
