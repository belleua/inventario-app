// v1.0 - Sidebar Navigation

import ProductCard from './ProductCard';

function ProductList({ products, onDelete, onEdit }) {
  if (products.length === 0) {
    return (
      <div className="text-center py-5">
        <p style={{fontSize: '3rem'}}>📦</p>
        <p className="text-muted">No hay productos aún. ¡Agrega el primero!</p>
      </div>
    );
  }

  return (
    <div className="table-responsive">
      <table className="table" style={{fontSize: '0.9rem'}}>
        <thead>
          <tr style={{color: '#888', borderBottom: '2px solid #f0f0f0'}}>
            <th className="pb-3">Producto</th>
            <th className="pb-3">Categoría</th>
            <th className="pb-3">Precio</th>
            <th className="pb-3">Stock</th>
            <th className="pb-3">Estado</th>
            <th className="pb-3">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {products.map(p => (
            <ProductCard key={p.id} product={p} onDelete={onDelete} onEdit={onEdit} />
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProductList;