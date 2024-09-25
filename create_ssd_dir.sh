for i in {0..23}; do
  device="/dev/nvme${i}n1"
  partition="${device}p1"
  mount_point="/data/9a3-$(printf "%02d" $((i+1)))"

  # 检查是否已有分区和挂载点
  if ! lsblk | grep -q "${partition}"; then
    echo "正在对 $device 进行分区..."
    # 创建一个主分区
    sudo parted $device mklabel gpt -s
    sudo parted $device mkpart primary xfs 0% 100% -s

    # 格式化为 XFS
    echo "格式化 $partition 为 XFS 文件系统..."
    sudo mkfs.xfs ${partition}

    # 创建挂载点
    sudo mkdir -p $mount_point

    # 挂载分区
    echo "挂载 $partition 到 $mount_point"
    sudo mount ${partition} $mount_point

    # 将挂载信息写入 /etc/fstab
    echo "${partition}  $mount_point  xfs  defaults  0  0" | sudo tee -a /etc/fstab
  else
    echo "$device 已分区并挂载。"
  fi
done
