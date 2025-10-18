async function submitFeedback(e) {
  e.preventDefault();
  const form = e.target;
  const data = {
    parent_name: form.parent_name.value || null,
    parent_email: form.parent_email.value || null,
    text: form.text.value
  };
  const res = await fetch('/api/feedback', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    alert('Error: ' + (err.detail || res.statusText));
    return;
  }
  const item = await res.json();
  form.reset();
  const out = document.getElementById('result');
  out.innerHTML = `
    <div class="card" style="margin-top:12px">
      <h2>Submitted ✔</h2>
      <div><strong>Sentiment:</strong> <span class="badge ${badgeClass(item.sentiment)}">${item.sentiment}</span></div>
      <div><strong>Department:</strong> <span class="badge">${item.department}</span></div>
      <div style="margin-top:6px;color:#a7b1d6">Your feedback has been routed and stored.</div>
    </div>
  `;
}

function badgeClass(sentiment) {
  if (sentiment === 'positive') return 'success';
  if (sentiment === 'negative') return 'danger';
  return 'neutral';
}

async function loadAdminTable() {
  const sentiment = document.getElementById('filter_sentiment')?.value || '';
  const department = document.getElementById('filter_department')?.value || '';
  const qs = new URLSearchParams();
  if (sentiment) qs.set('sentiment', sentiment);
  if (department) qs.set('department', department);
  const res = await fetch('/api/feedback' + (qs.toString() ? '?' + qs.toString() : ''));
  const items = await res.json();
  const tbody = document.getElementById('tbody');
  tbody.innerHTML = '';
  for (const it of items) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${it.id}</td>
      <td>${escapeHtml(it.parent_name || '')}</td>
      <td>${escapeHtml(it.parent_email || '')}</td>
      <td>${escapeHtml(it.text)}</td>
      <td><span class="badge ${badgeClass(it.sentiment)}">${it.sentiment}</span></td>
      <td><span class="badge">${it.department}</span></td>
      <td>${new Date(it.created_at).toLocaleString()}</td>
    `;
    tbody.appendChild(tr);
  }
  document.getElementById('count').textContent = items.length;
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, m => (
    {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]
  ));
}

window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('feedback_form');
  if (form) form.addEventListener('submit', submitFeedback);

  const admin = document.getElementById('adminPage');
  if (admin) {
    document.getElementById('filter_sentiment').addEventListener('change', loadAdminTable);
    document.getElementById('filter_department').addEventListener('change', loadAdminTable);
    document.getElementById('refresh').addEventListener('click', loadAdminTable);
    loadAdminTable();
  }
});
