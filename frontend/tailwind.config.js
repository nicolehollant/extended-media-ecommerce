module.exports = {
  theme: {
    zIndex: ["page", "nav", "dropdown", "modal", "onboarding"].reduce((obj, level, index) => {
      obj[`${level}-behind`] = (10 * index) - 1;
      obj[`${level}`] = 10 * index;
      obj[`${level}-front`] = (10 * index) + 1;
      return obj
    }, {}),
    extend: {
      width: {
        "min": "min-content",
        "max": "max-content",
      },
      height: {
        "min": "min-content",
        "max": "max-content",
      },
      borderRadius: {
        "xl": "0.75rem",
        "2xl": "1rem",
      }
    }
  },
  variants: {},
  plugins: [
    // transition 
    function({ addUtilities }) {
      const utils = {}
      const curves = ['', '-in', '-out', '-in-out']
      for(const curve of curves) {
        utils[`.ease${curve}-slow`] = { "transition": `all 1s ease${curve}` };
        utils[`.ease${curve}`] = { "transition": `all 0.3s ease${curve}` };
        utils[`.ease${curve}-fast`] = { "transition": `all 0.1s ease${curve}` };
      }
      addUtilities(utils)
    },
    // flex
    function({ addUtilities }) {
      const utils = {
        '.flex-center': {
          'display': 'flex',
          'align-items': 'center',
          'justify-content': 'center',
        },
        '.flex-col-center': {
          'display': 'flex',
          'align-items': 'center',
          'justify-content': 'center',
          'flex-direction': 'column',
        },
      }
      addUtilities(utils)
    }

  ],
  important: true
}
