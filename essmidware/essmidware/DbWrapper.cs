using System;
using System.Collections.Generic;
using Microsoft.Extensions.CommandLineUtils;
using Microsoft.VisualStudio.SourceSafe.Interop;

namespace ess.midware.essharp
{
    public class DbWrapper
    {
        public static VSSDatabase Db { get; } = new VSSDatabase();
        public static DbWrapper Current { get; } = new DbWrapper();

        public void Connect(string configfile, string user = "", string password = "")
        {
            Db.Open(configfile, user, password);
        }

        private Dictionary<string, object> ItemInfo(VSSItem item)
        {
            Dictionary<string, object> props = new Dictionary<string, object>(8);
            if (item.Type == 0)    // for projects
            {
                props.Add("type", "project");
                props.Add("size", item.Items.Count + " item");
            }
            else    // for files
            {
                props.Add("type", "file");
                props.Add("local_space", item.LocalSpec);
                props.Add("encoding", item.Encoding);
                props.Add("size", item.Size);
            }
            props.Add("version_number", item.VersionNumber);
            props.Add("deleted", item.Deleted);

            Dictionary<string, string> versionInfo = new Dictionary<string, string>(4);
            versionInfo.Add("user_name", item.VSSVersion.Username);
            versionInfo.Add("version_number", item.VSSVersion.VersionNumber.ToString());
            versionInfo.Add("comment", item.VSSVersion.Comment);
            versionInfo.Add("action", item.VSSVersion.Action);
            versionInfo.Add("date", item.VSSVersion.Date.ToString());
            props.Add("version_info", versionInfo);

            return props;
        }

        public string Items(string path = "$/")
        {
            VSSItem item = Db.VSSItem[path];
            Dictionary<string, object> subitems = new Dictionary<string, object>(8);
            foreach (VSSItem sub in item.Items)
            {
                subitems.Add(sub.Name, this.ItemInfo(sub));
            }
            return Util.JsonSerialize(subitems);
        }

        public string ItemDetail(string path = "$/")
        {
            VSSItem item = Db.VSSItem[path];
            return Util.JsonSerialize(this.ItemInfo(item));
        }

        public string SubNames(string path = "$/")
        {
            VSSItem item = Db.VSSItem[path];
            Dictionary<string, object> subitems = new Dictionary<string, object>(8);
            foreach (VSSItem sub in item.Items)
            {
                Dictionary<string, object> props = new Dictionary<string, object>(8);
                if (sub.Type == 0)    // for projects
                {
                    props.Add("type", "project");
                }
                else    // for files
                {
                    props.Add("type", "file");
                    props.Add("ischeckout", sub.IsCheckedOut == 0 ? false : true);
                }

                subitems.Add(sub.Name, props);
            }
            return Util.JsonSerialize(subitems);
        }

        public string FileStatus(string fullname)
        {
            VSSItem item = Db.VSSItem[fullname];
            Dictionary<string, object> status = new Dictionary<string, object>(3);

            status.Add("ischeckout", item.IsCheckedOut == 0 ? false : true);
            status.Add("encoding", item.Encoding);
            status.Add("local_space", item.LocalSpec);
            status.Add("size", item.Size);
            status.Add("version_number", item.VersionNumber);
            status.Add("deleted", item.Deleted);
            Dictionary<string, string> versionInfo = new Dictionary<string, string>(4);
            versionInfo.Add("user_name", item.VSSVersion.Username);
            versionInfo.Add("version_number", item.VSSVersion.VersionNumber.ToString());
            versionInfo.Add("comment", item.VSSVersion.Comment);
            versionInfo.Add("action", item.VSSVersion.Action);
            versionInfo.Add("date", item.VSSVersion.Date.ToString());
            status.Add("version_info", versionInfo);

            return Util.JsonSerialize(status);
        }


        static void Main(string[] args)
        {
            CommandLineApplication cmd_app = new CommandLineApplication();
            cmd_app.Description = "essharp: a cmd tool for vss with c sharp";
            cmd_app.Name = "essharp";
            cmd_app.Option("-l | --list", "list subitems", CommandOptionType.SingleValue);
            cmd_app.Option("-s | --status", "item's status", CommandOptionType.SingleValue);
            cmd_app.Option("-n | --names", "item's names", CommandOptionType.SingleValue);
            cmd_app.Option("-d | --detail", "item's detail", CommandOptionType.SingleValue);
            cmd_app.Option("-g | --get", "get files by full name", CommandOptionType.MultipleValue);

            cmd_app.HelpOption("-? | -h | --help");
            cmd_app.Execute(args);

            string ssini = Environment.GetEnvironmentVariable("SSDIR");
            // Current.Connect(ssini, "Cai.zfeng", "#fujitsu7864");
            Current.Connect(ssini);

            var opts = cmd_app.GetOptions();
            foreach (var opt in opts)
            {
                if (opt.Values.Count > 0)
                {
                    switch (opt.LongName)
                    {
                        case "list":
                            Current.List(opt.Value());
                            break;
                        case "status":
                            Current.GetFileStatus(opt.Value());
                            break;
                        case "names":
                            Current.GetSubNames(opt.Value());
                            break;
                        case "get":
                            Current.GetFiles(opt.Values[0], opt.Values[1]);
                            break;
                        case "detail":
                            Current.GetItemDetail(opt.Value());
                            break;
                    }
                }
            }
        }

        public void List(string fullname)
        {
            Console.WriteLine(this.Items(fullname));
        }

        public void GetFiles(string fullname, string output)
        {
            Db.VSSItem[fullname].Get(output);
        }

        public void GetFileStatus(string fullname)
        {
            Console.WriteLine(this.FileStatus(fullname));
        }

        public void GetSubNames(string path = "$/")
        {
            Console.WriteLine(this.SubNames(path));
        }

        public void GetItemDetail(string path = "$/")
        {
            Console.WriteLine(this.ItemDetail(path));
        }
    }
}
