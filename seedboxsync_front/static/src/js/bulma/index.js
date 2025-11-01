/**
 * Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */
import "./navbar";
import * as bulmaToast from "bulma-toast";

bulmaToast.setDefaults({
  type: 'is-success',
  duration: 10000,
  position: 'bottom-right',
  dismissible: false,
  pauseOnHover: true,
  closeOnClick: true,
  opacity: 1,
});

bulmaToast.toast({
  message: "Hello There",
  type: "is-success",
});