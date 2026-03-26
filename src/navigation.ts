import { getPermalink, getAsset } from './utils/permalinks';

export const headerData = {
  links: [
    { text: 'Services', href: getPermalink('/#services') },
    {
      text: 'Secteurs',
      links: [
        { text: 'Artisan / BTP', href: getPermalink('/automatisation/artisan-batiment') },
        { text: 'Cabinet Comptable', href: getPermalink('/automatisation/cabinet-comptable') },
        { text: 'Agence Immobilière', href: getPermalink('/automatisation/agence-immobiliere') },
        { text: 'Tous les secteurs', href: getPermalink('/automatisation') },
      ],
    },
    { text: 'Comment ça marche', href: getPermalink('/#process') },
    { text: 'FAQ', href: getPermalink('/#faq') },
    { text: 'Contact', href: getPermalink('/contact') },
  ],
  actions: [{ text: 'Prendre contact', href: getPermalink('/contact'), variant: 'primary' }],
};

export const footerData = {
  links: [
    {
      title: 'Services',
      links: [
        { text: 'Audit processus', href: '/#services' },
        { text: 'Automatisation PME', href: '/automatisation' },
        { text: 'Intégration IA', href: '/#services' },
      ],
    },
    {
      title: 'Secteurs',
      links: [
        { text: 'Artisan / BTP', href: '/automatisation/artisan-batiment' },
        { text: 'Cabinet Comptable', href: '/automatisation/cabinet-comptable' },
        { text: 'Agence Immobilière', href: '/automatisation/agence-immobiliere' },
      ],
    },
    {
      title: 'Ressources',
      links: [
        { text: 'Tarifs', href: '/tarifs' },
        { text: 'Glossaire', href: '/glossaire' },
        { text: 'Audit processus', href: '/audit-processus' },
      ],
    },
    {
      title: 'Agence',
      links: [
        { text: 'À propos', href: '/about' },
        { text: 'Contact', href: '/contact' },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'Mentions légales', href: getPermalink('/terms') },
    { text: 'Politique de confidentialité', href: getPermalink('/privacy') },
  ],
  socialLinks: [
    { ariaLabel: 'LinkedIn', icon: 'tabler:brand-linkedin', href: '#' },
  ],
  footNote: `© ${new Date().getFullYear()} UpgradR. Tous droits réservés.`,
};
