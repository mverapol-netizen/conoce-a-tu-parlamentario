(() => {
  const parseCsv = (text) => {
    const source = String(text || '').replace(/^\uFEFF/, '');
    const rows = [];
    let row = [];
    let field = '';
    let quoted = false;

    for (let i = 0; i < source.length; i += 1) {
      const ch = source[i];
      if (quoted) {
        if (ch === '"') {
          if (source[i + 1] === '"') {
            field += '"';
            i += 1;
          } else {
            quoted = false;
          }
        } else {
          field += ch;
        }
        continue;
      }
      if (ch === '"') {
        quoted = true;
      } else if (ch === ',') {
        row.push(field);
        field = '';
      } else if (ch === '\n') {
        row.push(field.replace(/\r$/, ''));
        if (row.some((value) => value !== '')) rows.push(row);
        row = [];
        field = '';
      } else {
        field += ch;
      }
    }
    if (field.length || row.length) {
      row.push(field.replace(/\r$/, ''));
      if (row.some((value) => value !== '')) rows.push(row);
    }
    if (!rows.length) return [];
    const headers = rows.shift().map((value) => value.trim());
    return rows.map((values) => {
      const record = {};
      headers.forEach((header, index) => { record[header] = values[index] ?? ''; });
      return record;
    });
  };

  const fetchCsv = async (url) => {
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) throw new Error(`No se pudo cargar ${url} (${response.status})`);
    return parseCsv(await response.text());
  };

  const normalize = (value) => String(value || '')
    .toLocaleLowerCase('es-CL')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const formatDate = (value) => {
    if (!value) return 'Sin fecha';
    const parts = String(value).slice(0, 10).split('-');
    if (parts.length !== 3) return value;
    const [year, month, day] = parts;
    return `${day}-${month}-${year}`;
  };

  window.CSV_UTILS = { parseCsv, fetchCsv, normalize, escapeHtml, formatDate };
})();
