# Troubleshooting

Common issues and solutions for DClaw Design.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-design

# Check logs
kubectl logs -n dclaw-design deployment/dclaw-design-backend

# Check database
kubectl get clusters -n dclaw-design
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
