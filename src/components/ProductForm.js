// Feature:         
// Form Component  


import { useState, useEffect } from 'react';

function ProductForm({ onAdd, onUpdate, editingProduct, onCancel }) {
  const [form, setForm] = useState({
    name: '', category: '', price: '', stock: '', status: 'disponible'
  });

  useEffect(() => {
    if (editingProduct) setForm(editingProduct);
    else setForm({ name: '', category: '', price: '', stock: '', status: 'disponible' });
  }, [editingProduct]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.name || !form.price) return alert('Nombre y precio son requeridos');
    if (editingProduct) onUpdate(form);
    else onAdd(form);
    setForm({ name: '', category: '', price: '', stock: '', status: 'disponible' });
  };

  return (
    <div className="row g-3">
      <div className="col-md-4">
        <input name="name" value={form.name} onChange={handleChange}
          className="form-control" placeholder="Nombre del producto" />
      </div>
      <div className="col-md-3">
        <input name="category" value={form.category} onChange={handleChange}
          className="form-control" placeholder="Categoría" />
      </div>
      <div className="col-md-2">
        <input name="price" value={form.price} onChange={handleChange} type="number"
          className="form-control" placeholder="Precio (RD$)" />
      </div>
      <div className="col-md-1">
        <input name="stock" value={form.stock} onChange={handleChange} type="number"
          className="form-control" placeholder="Stock" />
      </div>
      <div className="col-md-2">
        <select name="status" value={form.status} onChange={handleChange} className="form-select">
          <option value="disponible"> Disponible</option>
          <option value="agotado"> Agotado</option>
          <option value="bajo_stock"> Bajo Stock</option>
        </select>
      </div>
      <div className="col-12 d-flex gap-2">
        <button onClick={handleSubmit} className="btn-primary-custom">
          {editingProduct ? 'Guardar cambios' : '+ Agregar producto'}
        </button>
        {editingProduct && (
          <button onClick={onCancel} className="btn btn-outline-secondary" style={{borderRadius: '10px'}}>
            Cancelar
          </button>
        )}
      </div>
    </div>
  );
}

export default ProductForm;
