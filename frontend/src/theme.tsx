import React from "react";
import { createTheme } from "@mui/material";
import { Link as RouterLink, LinkProps as RouterLinkProps } from 'react-router-dom';
import { LinkProps } from '@mui/material/Link';
import TextField from '@mui/material/TextField';

const LinkBehavior = React.forwardRef<
  HTMLAnchorElement,
  Omit<RouterLinkProps, 'to'> & { href: RouterLinkProps['to'] }
>((props, ref) => {
  const { href, ...other } = props;
  return <RouterLink ref={ref} to={href} {...other} />;
});

const theme = createTheme({
  palette: {
    primary: {
      main: "#6088EC"
    },
    secondary: {
      main: "#A0A4BF"
    },
    text: {
      primary: "#6088EC",
      secondary: "#A0A4BF"
    }
  },
  components: {
    MuiLink: {
      defaultProps: {
        component: LinkBehavior,
      } as LinkProps,
    },
    MuiButtonBase: {
      defaultProps: {
        LinkComponent: LinkBehavior,
      },
    },
    MuiTextField: {
      defaultProps: {
        sx: {
          input: {
            color: "black"
          },
          textarea: {
            color: "black"
          }
        }
      }
    }
  },
});

export default theme;