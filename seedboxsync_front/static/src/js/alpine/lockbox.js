 /**
 * Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */

/**
 * Build AlpineJS lock box components.
 * @param {*} apiUrl
 * @param {*} refreshMs
 * @returns
 */
export function lockBoxComponent(url, refreshMs = 30000) {
  return {
    loading: true,
    error: null,
    lockData: null,
    lockMessage: "",

    async init() {
      await this.loadLock();
      if (refreshMs > 0) {
        setInterval(() => this.loadLock(), refreshMs);
      }
    },

    async loadLock() {
      this.loading = true;
      this.error = null;
      try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        const json = await res.json();
        this.lockData = json.data;

        if (this.lockData.locked) {
          this.lockMessage = `Lock since ${new Date(
            this.lockData.locked_at
          ).toLocaleString()}`;
        } else {
          this.lockMessage = `Unlock since ${new Date(
            this.lockData.unlocked_at
          ).toLocaleString()}`;
        }
      } catch (e) {
        this.error = "Error loading lock status";
        console.error(e);
      } finally {
        this.loading = false;
      }
    },
  };
}