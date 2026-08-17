/* ------------------------------------------------------------------
   CẤU HÌNH — chỉ cần sửa OWNER và REPO cho đúng repo GitHub của bạn.
   Người dùng và PIN KHÔNG nằm ở đây — chúng nằm trong keys.json,
   tạo bằng lệnh:  python3 scripts/init_crypto.py --users "NAM:...:admin,AHUY:...:oz" ...
   ------------------------------------------------------------------ */
window.OZ_CONFIG = {
  OWNER:  "NAM-VOPH",       // <-- tên tài khoản GitHub của bạn
  REPO:   "oz-todo",        // <-- tên repository
  BRANCH: "main",

  AUTOSYNC_MS: 120000,      // đồng bộ tự động 2 phút sau thao tác cuối
  MAX_FILE_MB: 5            // giới hạn dung lượng file đính kèm
};
