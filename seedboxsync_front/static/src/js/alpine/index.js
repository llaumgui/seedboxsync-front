/**
 * Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */
import Alpine from "alpinejs";
import { TableComponent } from "./table";
import { TablePaginedComponent } from "./table_pagined";
import { LockBoxComponent } from "./lockbox";
import { ModalConfirmCallComponent, OpenModalConfirmCall } from "./modal";

window.TableComponent = TableComponent;
window.TablePaginedComponent = TablePaginedComponent;
window.LockBoxComponent = LockBoxComponent;
window.ModalConfirmCallComponent = ModalConfirmCallComponent;
window.OpenModalConfirmCall = OpenModalConfirmCall;

window.Alpine = Alpine;
Alpine.start();