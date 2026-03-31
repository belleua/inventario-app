import { useState } from 'react';
import ProductForm from './components/ProductForm';
import ProductList from './components/ProductList';
import './App.css';

function App() {
  const [products, setProducts] = useState([]);
  const [editingProduct, setEditingProduct] = useState(null);
  const [activeMenu, setActiveMenu] = useState('dashboard');

  const addProduct = (product) => {
    setProducts([...products, { ...product, id: Date.now() }]);
  };

  const deleteProduct = (id) => {
    setProducts(products.filter(p => p.id !== id));
  };

  const updateProduct = (updatedProduct) => {
    setProducts(products.map(p => p.id === updatedProduct.id ? updatedProduct : p));
    setEditingProduct(null);
  };

  const disponibles = products.filter(p => p.status === 'disponible').length;
  const agotados = products.filter(p => p.status === 'agotado').length;
  const bajoStock = products.filter(p => p.status === 'bajo_stock').length;

  return (
    <div style={{display: 'flex'}}>
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-logo"> Inven<span>tario</span></div>
        <ul className="sidebar-menu">
          {[
            { id: 'dashboard', icon: '🏠', label: 'Dashboard' },
            { id: 'inventario', icon: '📦', label: 'Inventario' },
            { id: 'productos', icon: '🛍️', label: 'Productos' },
          ].map(item => (
            <li key={item.id}
              className={activeMenu === item.id ? 'active' : ''}
              onClick={() => setActiveMenu(item.id)}>
              {item.icon} &nbsp; {item.label}
            </li>
          ))}
        </ul>
      </div>

      {/* Main Content */}
      <div className="main-content" style={{flex: 1}}>
        {/* Topbar */}
        <div className="topbar">
          <div>
            <h4>Panel de Inventario</h4>
            <p>Resumen de tus productos</p>
          </div>
        </div>

        {/* Stats - siempre visibles */}
        <div className="row g-3 mb-4">
          {[
            { label: 'Total Productos', value: products.length, color: '#667eea' },
            { label: 'Disponibles', value: disponibles, color: '#27ae60' },
            { label: 'Bajo Stock', value: bajoStock, color: '#f39c12' },
            { label: 'Agotados', value: agotados, color: '#e74c3c' },
          ].map((stat, i) => (
            <div className="col-md-3" key={i}>
              <div className="stat-card" style={{borderTopColor: stat.color}}>
                <div className="stat-value" style={{color: stat.color}}>{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Dashboard */}
        {activeMenu === 'dashboard' && (
          <div className="section-card text-center py-5">
            <p style={{fontSize: '3rem'}}></p>
            <h5 className="fw-bold">Bienvenida al Panel</h5>
            <p className="text-muted">Selecciona <strong>Inventario</strong> para gestionar productos.</p>
          </div>
        )}

        {/* Inventario - Formulario + Lista */}
        {activeMenu === 'inventario' && (
          <>
            <div className="section-card">
              <div className="section-title">
                {editingProduct ? 'Editar Producto' : ' Agregar Producto'}
              </div>
              <ProductForm
                onAdd={addProduct}
                onUpdate={updateProduct}
                editingProduct={editingProduct}
                onCancel={() => setEditingProduct(null)}
              />
            </div>
            <div className="section-card">
              <div className="section-title"> Lista de Productos</div>
              <ProductList
                products={products}
                onDelete={deleteProduct}
                onEdit={setEditingProduct}
              />
            </div>
          </>
        )}

        {/* Productos - Solo la lista */}
        {activeMenu === 'productos' && (
          <div className="section-card">
            <div className="section-title"> Todos los Productos</div>
            <ProductList
              products={products}
              onDelete={deleteProduct}
              onEdit={(p) => { setEditingProduct(p); setActiveMenu('inventario'); }}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;