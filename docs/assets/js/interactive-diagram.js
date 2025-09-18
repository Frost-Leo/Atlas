/**
 * Interactive Diagram Component
 * Provides draggable nodes for architecture diagrams
 */

class InteractiveDiagram {
    constructor(containerId, config) {
        this.container = document.getElementById(containerId);
        this.config = config;
        this.nodes = [];
        this.connections = [];
        this.isDragging = false;
        this.dragNode = null;
        this.offset = { x: 0, y: 0 };
        
        this.init();
    }
    
    init() {
        this.container.style.position = 'relative';
        this.container.style.width = '100%';
        this.container.style.height = '500px';
        this.container.style.border = '1px solid #ddd';
        this.container.style.borderRadius = '8px';
        this.container.style.backgroundColor = '#fafafa';
        this.container.style.overflow = 'hidden';
        
        this.createNodes();
        this.createConnections();
        this.bindEvents();
    }
    
    createNodes() {
        this.config.nodes.forEach((nodeConfig, index) => {
            const node = document.createElement('div');
            node.className = 'diagram-node';
            node.textContent = nodeConfig.label;
            node.style.cssText = `
                position: absolute;
                left: ${nodeConfig.x}px;
                top: ${nodeConfig.y}px;
                width: ${nodeConfig.width || 120}px;
                height: ${nodeConfig.height || 40}px;
                background: ${nodeConfig.color || '#4CAF50'};
                color: white;
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: move;
                font-size: 12px;
                font-weight: bold;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                user-select: none;
                z-index: 10;
                transition: transform 0.1s ease;
            `;
            
            node.dataset.nodeId = index;
            this.container.appendChild(node);
            this.nodes.push({
                element: node,
                config: nodeConfig,
                id: index
            });
        });
    }
    
    createConnections() {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 5;
        `;
        
        this.container.appendChild(svg);
        this.svg = svg;
        
        // Add arrowhead marker definition
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.setAttribute('id', 'arrowhead');
        marker.setAttribute('markerWidth', '10');
        marker.setAttribute('markerHeight', '7');
        marker.setAttribute('refX', '9');
        marker.setAttribute('refY', '3.5');
        marker.setAttribute('orient', 'auto');
        
        const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        polygon.setAttribute('points', '0 0, 10 3.5, 0 7');
        polygon.setAttribute('fill', '#666');
        
        marker.appendChild(polygon);
        defs.appendChild(marker);
        this.svg.appendChild(defs);
        
        this.updateConnections();
    }
    
    updateConnections() {
        // Clear existing connections
        this.svg.innerHTML = '';
        
        this.config.connections.forEach(conn => {
            const fromNode = this.nodes[conn.from];
            const toNode = this.nodes[conn.to];
            
            if (fromNode && toNode) {
                const line = this.createConnection(fromNode, toNode);
                this.svg.appendChild(line);
            }
        });
    }
    
    createConnection(fromNode, toNode) {
        // Use element positions directly since getBoundingClientRect might not work in all contexts
        const fromX = parseInt(fromNode.element.style.left) + (fromNode.config.width || 120) / 2;
        const fromY = parseInt(fromNode.element.style.top) + (fromNode.config.height || 40) / 2;
        const toX = parseInt(toNode.element.style.left) + (toNode.config.width || 120) / 2;
        const toY = parseInt(toNode.element.style.top) + (toNode.config.height || 40) / 2;
        
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', fromX);
        line.setAttribute('y1', fromY);
        line.setAttribute('x2', toX);
        line.setAttribute('y2', toY);
        line.setAttribute('stroke', '#666');
        line.setAttribute('stroke-width', '2');
        line.setAttribute('marker-end', 'url(#arrowhead)');
        
        return line;
    }
    
    bindEvents() {
        this.nodes.forEach(node => {
            node.element.addEventListener('mousedown', (e) => {
                this.startDrag(e, node);
            });
        });
        
        document.addEventListener('mousemove', (e) => {
            this.drag(e);
        });
        
        document.addEventListener('mouseup', () => {
            this.endDrag();
        });
    }
    
    startDrag(e, node) {
        this.isDragging = true;
        this.dragNode = node;
        
        const rect = node.element.getBoundingClientRect();
        this.offset.x = e.clientX - rect.left;
        this.offset.y = e.clientY - rect.top;
        
        node.element.style.transform = 'scale(1.05)';
        node.element.style.zIndex = '20';
        
        e.preventDefault();
    }
    
    drag(e) {
        if (!this.isDragging || !this.dragNode) return;
        
        const containerRect = this.container.getBoundingClientRect();
        const x = e.clientX - containerRect.left - this.offset.x;
        const y = e.clientY - containerRect.top - this.offset.y;
        
        // Constrain to container bounds
        const maxX = this.container.offsetWidth - this.dragNode.element.offsetWidth;
        const maxY = this.container.offsetHeight - this.dragNode.element.offsetHeight;
        
        const constrainedX = Math.max(0, Math.min(x, maxX));
        const constrainedY = Math.max(0, Math.min(y, maxY));
        
        this.dragNode.element.style.left = constrainedX + 'px';
        this.dragNode.element.style.top = constrainedY + 'px';
        
        this.updateConnections();
    }
    
    endDrag() {
        if (this.dragNode) {
            this.dragNode.element.style.transform = 'scale(1)';
            this.dragNode.element.style.zIndex = '10';
        }
        
        this.isDragging = false;
        this.dragNode = null;
    }
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InteractiveDiagram;
}