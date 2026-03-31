// v1.0 - Product Card

function ProductCard({ product, onDelete, onEdit }) {
  const statusConfig = {
    disponible: { label: 'Disponible', cls: 'badge-disponible' },
    bajo_stock: { label: 'Bajo Stock', cls: 'badge-bajo_stock' },
    agotado:    { label: 'Agotado',    cls: 'badge-agotado' }
  };

  const config = statusConfig[product.status] || statusConfig.disponible;

  return (
    <tr style={{borderBottom: '1px solid #f0f0f0'}}>
      <td className="py-3 fw-600">{product.name}</td>
      <td className="py-3 text-muted">{product.category || '—'}</td>
      <td className="py-3 fw-600">RD$ {Number(product.price).toLocaleString()}</td>
      <td className="py-3">{product.stock || 0}</td>
      <td className="py-3">
        <span className={`badge-status ${config.cls}`}>{config.label}</span>
      </td>
      <td className="py-3">
        <button className="btn-icon me-1" onClick={() => onEdit(product)}>✏️</button>
        <button className="btn-icon" onClick={() => onDelete(product.id)}>🗑️</button>
      </td>
    </tr>
  );
}

export default ProductCard;