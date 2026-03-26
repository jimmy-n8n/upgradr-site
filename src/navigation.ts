import { getPermalink, getAsset } from './utils/permalinks';

export const headerData = {
  links: [
    { text: 'Services', href: getPermalink('/#services') },
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
        { text: 'Automatisation', href: '/#services' },
        { text: 'Intégration IA', href: '/#services' },
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
