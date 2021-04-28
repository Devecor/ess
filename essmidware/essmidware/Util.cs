using System.Collections.Generic;
using System.Web.Script.Serialization;

namespace ess.midware.essharp
{
    class Util
    {
        private static JavaScriptSerializer serializer = new JavaScriptSerializer();
        public static string JsonSerialize(Dictionary<string, object> dict)
        {
            return serializer.Serialize(dict);
        }

        public static string JsonSerialize(List<Dictionary<string, string>> list)
        {
            return serializer.Serialize(list);
        }
    }
}
